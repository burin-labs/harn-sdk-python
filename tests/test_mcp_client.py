import asyncio
import json

import httpx
import pytest

from harn import AsyncHarnClient, HarnClient
from harn._codegen import protocol as facts
from harn._mcp_client import AsyncMcpClient, McpClient
from harn._mcp_protocol import response_result
from harn.bindings import BindingError


class Peer:
    def __init__(self, mode="direct"):
        self.mode = mode
        self.requests = []

    def respond(self, request):
        body = json.loads(request.content)
        self.requests.append((request, body))
        method = body["method"]
        assert request.headers[facts.MCP_HEADER_METHOD] == method
        assert (
            request.headers[facts.MCP_HEADER_PROTOCOL_VERSION]
            == facts.MCP_PROTOCOL_VERSION
        )
        assert "Harn-Agents-Protocol-Version" not in request.headers
        meta = body["params"]["_meta"]
        assert meta[facts.MCP_META_KEY_PROTOCOL_VERSION] == facts.MCP_PROTOCOL_VERSION
        assert (
            facts.MCP_TASKS_EXTENSION_ID
            in meta[facts.MCP_META_KEY_CLIENT_CAPABILITIES]["extensions"]
        )
        if method == facts.MCP_METHOD_SERVER_DISCOVER:
            assert "authorization" not in request.headers
            result = {
                "resultType": "complete",
                "supportedVersions": [facts.MCP_PROTOCOL_VERSION],
                "capabilities": {"tools": {}},
            }
        elif method == facts.MCP_METHOD_TOOLS_CALL:
            assert request.headers[facts.MCP_HEADER_NAME] == "echo"
            assert request.headers["authorization"] == "Bearer synthetic-sdk-key"
            if self.mode == "direct":
                result = {
                    "resultType": "complete",
                    "isError": False,
                    "structuredContent": {"result": "ok"},
                }
            elif self.mode == "missing-result":
                return httpx.Response(200, json={"jsonrpc": "2.0", "id": body["id"]})
            elif self.mode == "wrong-response-id":
                return httpx.Response(
                    200, json={"jsonrpc": "2.0", "id": "wrong", "result": {}}
                )
            elif self.mode == "null-result":
                return httpx.Response(
                    200, json={"jsonrpc": "2.0", "id": body["id"], "result": None}
                )
            else:
                result = {"resultType": "task", "taskId": "owned-task"}
        elif method == facts.MCP_METHOD_TASKS_GET:
            assert body["params"]["taskId"] == "owned-task"
            assert request.headers[facts.MCP_HEADER_NAME] == "owned-task"
            result = {
                "resultType": "complete",
                "taskId": "owned-task",
                "status": "completed",
                "result": {
                    "resultType": "complete",
                    "isError": False,
                    "structuredContent": {"result": "ok"},
                },
            }
            if self.mode == "task-status-missing":
                result.pop("status")
            elif self.mode == "task-result-missing":
                result.pop("result")
            elif self.mode == "task-wrong-id":
                result["taskId"] = "other-task"
        else:
            raise AssertionError(f"unexpected method {method}")
        return httpx.Response(
            200, json={"jsonrpc": "2.0", "id": body["id"], "result": result}
        )


@pytest.mark.parametrize("mode", ["direct", "task"])
def test_sync_direct_and_server_selected_tasks_reuse_sdk_auth_transport(mode):
    peer = Peer(mode)
    with pytest.warns(UserWarning, match="base_url overridden"):
        client = HarnClient(
            base_url="http://localhost",
            token="synthetic-sdk-key",
            client=httpx.Client(
                base_url="http://localhost", transport=httpx.MockTransport(peer.respond)
            ),
        )
    with client:
        assert McpClient(client).call("echo", {"text": "ok"})["structuredContent"] == {
            "result": "ok"
        }
    methods = [body["method"] for _, body in peer.requests]
    assert methods == [
        facts.MCP_METHOD_SERVER_DISCOVER,
        facts.MCP_METHOD_TOOLS_CALL,
    ] + ([facts.MCP_METHOD_TASKS_GET] if mode == "task" else [])


@pytest.mark.asyncio
@pytest.mark.parametrize("mode", ["direct", "task"])
async def test_async_direct_and_server_selected_tasks_reuse_sdk_auth_transport(mode):
    peer = Peer(mode)
    with pytest.warns(UserWarning, match="base_url overridden"):
        client = AsyncHarnClient(
            base_url="http://localhost",
            token="synthetic-sdk-key",
            client=httpx.AsyncClient(
                base_url="http://localhost", transport=httpx.MockTransport(peer.respond)
            ),
        )
    async with client:
        assert (await AsyncMcpClient(client).call("echo", {"text": "ok"}))[
            "structuredContent"
        ] == {"result": "ok"}
    assert len(peer.requests) == (3 if mode == "task" else 2)


@pytest.mark.parametrize(
    "mode,code",
    [
        ("missing-result", "mcp_response_missing_result"),
        ("wrong-response-id", "mcp_response_identity"),
        ("null-result", "mcp_response_not_object"),
        ("task-status-missing", "mcp_task_status_unmeasured"),
        ("task-result-missing", "mcp_task_result_unmeasured"),
        ("task-wrong-id", "mcp_task_identity"),
    ],
)
def test_missing_and_mismatched_observations_cannot_become_success(mode, code):
    peer = Peer(mode)
    with HarnClient(
        base_url="http://localhost",
        client=httpx.Client(
            base_url="http://localhost", transport=httpx.MockTransport(peer.respond)
        ),
    ) as client:
        # These controls do not need a credential; Peer still measures whether the call reached it.
        client.token = "synthetic-sdk-key"
        with pytest.raises(BindingError) as failure:
            McpClient(client).call("echo", {})
    assert failure.value.code == code
    assert len(peer.requests) >= 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_selected,delivery_fails",
    [(False, False), (True, False), (True, True), (True, "rpc")],
)
async def test_http_cancellation_closes_the_exchange_and_only_known_tasks_send_cancel(
    task_selected, delivery_fails
):
    entered = asyncio.Event()
    blocked = asyncio.Event()
    closed = asyncio.Event()
    messages = []
    recovered = False

    async def respond(request):
        body = json.loads(request.content)
        messages.append(body)
        method = body["method"]
        if method == facts.MCP_METHOD_SERVER_DISCOVER:
            result = {
                "resultType": "complete",
                "supportedVersions": [facts.MCP_PROTOCOL_VERSION],
                "capabilities": {"tools": {}},
            }
        elif method == facts.MCP_METHOD_TOOLS_CALL:
            if recovered:
                result = {
                    "resultType": "complete",
                    "isError": False,
                    "structuredContent": "recovered",
                }
            elif task_selected:
                result = {"resultType": "task", "taskId": "owned-task"}
            else:
                entered.set()
                try:
                    await blocked.wait()
                finally:
                    closed.set()
                raise AssertionError("cancelled call resumed")
        elif method == facts.MCP_METHOD_TASKS_GET:
            entered.set()
            try:
                await blocked.wait()
            finally:
                closed.set()
            raise AssertionError("cancelled poll resumed")
        elif method == facts.MCP_METHOD_TASKS_CANCEL:
            if delivery_fails is True:
                return httpx.Response(
                    500,
                    json={"error": {"code": "fixture", "message": "delivery refused"}},
                )
            if delivery_fails == "rpc":
                return httpx.Response(
                    200,
                    json={
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "error": {"code": -32602, "message": "delivery refused"},
                    },
                )
            result = {"resultType": "complete"}
        else:
            raise AssertionError(method)
        return httpx.Response(
            200, json={"jsonrpc": "2.0", "id": body["id"], "result": result}
        )

    async with AsyncHarnClient(
        base_url="http://localhost",
        client=httpx.AsyncClient(
            base_url="http://localhost", transport=httpx.MockTransport(respond)
        ),
    ) as client:
        mcp = AsyncMcpClient(client)
        operation = asyncio.create_task(mcp.call("echo", {}))
        async with asyncio.timeout(30):
            await entered.wait()
            operation.cancel()
            with pytest.raises(asyncio.CancelledError) as cancellation:
                await operation
        assert closed.is_set()
        recovered = True
        assert (await mcp.call("echo", {}))["structuredContent"] == "recovered"
    notices = [
        body
        for body in messages
        if body["method"]
        in (facts.MCP_METHOD_TASKS_CANCEL, facts.MCP_METHOD_CANCELLED_NOTIFICATION)
    ]
    assert all(
        body["method"] != facts.MCP_METHOD_CANCELLED_NOTIFICATION for body in messages
    )
    if task_selected:
        assert len(notices) == 1
        assert notices[0]["params"]["taskId"] == "owned-task"
    else:
        assert notices == []
    if delivery_fails:
        assert (
            "MCP cancellation delivery was not acknowledged"
            in cancellation.value.__notes__
        )


def test_json_rpc_null_is_present_data_while_a_missing_result_is_unknown():
    assert (
        response_result(
            {"jsonrpc": "2.0", "id": "known", "result": None}, "known", "control"
        )
        is None
    )
    with pytest.raises(BindingError, match="mcp_response_missing_result"):
        response_result({"jsonrpc": "2.0", "id": "known"}, "known", "control")
