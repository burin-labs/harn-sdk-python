"""MCP selects a terminal response without waiting for stream EOF."""

import asyncio
import json
import math

import httpx
import pytest

from harn import AsyncHarnClient, HarnClient
from harn._codegen import protocol as facts
from harn._mcp_client import AsyncMcpClient, McpClient
from harn.bindings import BindingError


def frame(identity, result):
    return (
        'data: {"jsonrpc":"2.0","id":'
        + json.dumps(identity)
        + ',"result":'
        + result
        + "}\n\n"
    )


class SyncResponse(httpx.SyncByteStream):
    def __init__(self, content):
        self.content, self.closed = content.encode(), False

    def __iter__(self):
        yield self.content
        raise AssertionError("MCP read beyond its terminal response")

    def close(self):
        self.closed = True


class AsyncResponse(httpx.AsyncByteStream):
    def __init__(self, content):
        self.content, self.closed = content.encode(), False

    async def __aiter__(self):
        yield self.content
        raise AssertionError("MCP read beyond its terminal response")

    async def aclose(self):
        self.closed = True


RESULT = '{"resultType":"complete","structuredContent":{"integer":9223372036854775807,"negative_zero":-0}}'
PROGRESS = ': keepalive\r\ndata: {"jsonrpc":"2.0","method":"notifications/progress","params":{"progressToken":"probe","progress":1}}\r\n\r\n'


def assert_values(result):
    assert type(result["structuredContent"]["integer"]) is int
    assert result["structuredContent"]["integer"] == 9223372036854775807
    zero = result["structuredContent"]["negative_zero"]
    assert type(zero) is float and math.copysign(1, zero) == -1


@pytest.mark.parametrize("sse", [False, True])
def test_sync_json_and_sse_response_close_without_reading_past_terminal(sse):
    reached, streams = [], []

    def respond(request):
        assert set(request.headers["accept"].split(", ")) == {
            "application/json",
            "text/event-stream",
        }
        body = json.loads(request.content)
        reached.append(body["id"])
        response = frame(body["id"], RESULT)
        if sse:
            stream = SyncResponse(PROGRESS + response)
            streams.append(stream)
            return httpx.Response(
                200, headers={"content-type": "text/event-stream"}, stream=stream
            )
        return httpx.Response(
            200,
            headers={"content-type": "application/json"},
            content=response.removeprefix("data: "),
        )

    with HarnClient(
        base_url="http://localhost",
        client=httpx.Client(
            base_url="http://localhost", transport=httpx.MockTransport(respond)
        ),
    ) as transport:
        assert_values(
            McpClient(transport).rpc(
                facts.MCP_METHOD_TOOLS_CALL, {"name": "echo", "arguments": {}}
            )
        )
    assert len(reached) == 1
    assert all(stream.closed for stream in streams)


@pytest.mark.asyncio
@pytest.mark.parametrize("sse", [False, True])
async def test_async_json_and_sse_response_close_without_reading_past_terminal(sse):
    reached, streams = [], []

    def respond(request):
        assert set(request.headers["accept"].split(", ")) == {
            "application/json",
            "text/event-stream",
        }
        body = json.loads(request.content)
        reached.append(body["id"])
        response = frame(body["id"], RESULT)
        if sse:
            stream = AsyncResponse(PROGRESS + response)
            streams.append(stream)
            return httpx.Response(
                200, headers={"content-type": "text/event-stream"}, stream=stream
            )
        return httpx.Response(
            200,
            headers={"content-type": "application/json"},
            content=response.removeprefix("data: "),
        )

    async with AsyncHarnClient(
        base_url="http://localhost",
        client=httpx.AsyncClient(
            base_url="http://localhost", transport=httpx.MockTransport(respond)
        ),
    ) as transport:
        assert_values(
            await AsyncMcpClient(transport).rpc(
                facts.MCP_METHOD_TOOLS_CALL, {"name": "echo", "arguments": {}}
            )
        )
    assert len(reached) == 1
    assert all(stream.closed for stream in streams)


@pytest.mark.asyncio
async def test_task_prelude_is_observed_before_eof_and_cancel_targets_known_task():
    streams, cancelled = [], []
    polling = asyncio.Event()
    hold = asyncio.Event()

    async def respond(request):
        body = json.loads(request.content)
        method = body["method"]
        if method == facts.MCP_METHOD_SERVER_DISCOVER:
            result = {
                "resultType": "complete",
                "supportedVersions": [facts.MCP_PROTOCOL_VERSION],
                "capabilities": {"tools": {}},
            }
        elif method == facts.MCP_METHOD_TOOLS_CALL:
            stream = AsyncResponse(
                frame(body["id"], '{"resultType":"task","taskId":"recorded-task"}')
            )
            streams.append(stream)
            return httpx.Response(
                200, headers={"content-type": "text/event-stream"}, stream=stream
            )
        elif method == facts.MCP_METHOD_TASKS_GET:
            assert streams[0].closed
            assert body["params"]["taskId"] == "recorded-task"
            polling.set()
            await hold.wait()
            raise AssertionError("Task poll must be cancelled")
        elif method == facts.MCP_METHOD_TASKS_CANCEL:
            cancelled.append(body["params"]["taskId"])
            result = {"resultType": "complete"}
        else:
            raise AssertionError("Unexpected request")
        return httpx.Response(
            200, json={"jsonrpc": "2.0", "id": body["id"], "result": result}
        )

    async with AsyncHarnClient(
        base_url="http://localhost",
        client=httpx.AsyncClient(
            base_url="http://localhost", transport=httpx.MockTransport(respond)
        ),
    ) as transport:
        running = asyncio.create_task(AsyncMcpClient(transport).call("echo", {}))
        reached = asyncio.create_task(polling.wait())
        try:
            await asyncio.wait({running, reached}, return_when=asyncio.FIRST_COMPLETED)
            if running.done():
                await running
                raise AssertionError("Call completed without a task poll")
            assert polling.is_set()
            running.cancel()
            with pytest.raises(asyncio.CancelledError):
                await running
        finally:
            running.cancel()
            reached.cancel()
    assert cancelled == ["recorded-task"] and streams[0].closed


@pytest.mark.parametrize(
    "payload",
    [
        "",
        ": comment\n\n",
        "data: {}\n\n",
        'data: {"jsonrpc":"2.0","method":""}\n\n',
        "data: not-json\n\n",
        frame("unmeasured", RESULT).rstrip("\n"),
    ],
)
def test_empty_and_malformed_sse_cannot_become_success(payload):
    reached = []

    def respond(request):
        reached.append(request)
        return httpx.Response(
            200, headers={"content-type": "text/event-stream"}, content=payload
        )

    with (
        HarnClient(
            base_url="http://localhost",
            client=httpx.Client(
                base_url="http://localhost", transport=httpx.MockTransport(respond)
            ),
        ) as transport,
        pytest.raises(BindingError),
    ):
        McpClient(transport).rpc(
            facts.MCP_METHOD_TOOLS_CALL, {"name": "echo", "arguments": {}}
        )
    assert len(reached) == 1


@pytest.mark.parametrize("mode", ["wrong-id", "ambiguous"])
def test_sse_uses_existing_rpc_identity_and_ambiguity_owner(mode):
    def respond(request):
        body = json.loads(request.content)
        identity = "wrong-id" if mode == "wrong-id" else body["id"]
        response = {"jsonrpc": "2.0", "id": identity, "result": {}}
        if mode == "ambiguous":
            response["error"] = {"code": -32603, "message": "synthetic fault"}
        return httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content="data: " + json.dumps(response) + "\n\n",
        )

    with (
        HarnClient(
            base_url="http://localhost",
            client=httpx.Client(
                base_url="http://localhost", transport=httpx.MockTransport(respond)
            ),
        ) as transport,
        pytest.raises(
            BindingError,
            match="mcp_response_identity"
            if mode == "wrong-id"
            else "mcp_response_ambiguous",
        ),
    ):
        McpClient(transport).rpc(
            facts.MCP_METHOD_TOOLS_CALL, {"name": "echo", "arguments": {}}
        )
