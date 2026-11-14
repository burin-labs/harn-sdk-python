"""MCP calls over the existing SDK transport, including server-selected tasks."""

from __future__ import annotations

import asyncio
import threading
import time
import uuid

from pydantic import JsonValue, ValidationError

from ._codegen import protocol as facts
from ._mcp_protocol import McpHeaders, discovery_result, request_params, response_result
from .bindings import BindingError
from .client import AsyncHarnClient, HarnClient


def _body(
    method: str, params: dict[str, JsonValue], identity: str
) -> dict[str, JsonValue]:
    body: dict[str, JsonValue] = {
        "jsonrpc": "2.0",
        "method": method,
        "params": request_params(params),
    }
    body["id"] = identity
    return body


def _task_identity(result: dict[str, JsonValue]) -> str | None:
    if result.get("resultType") == "complete":
        return None
    identity = result.get("taskId")
    if (
        result.get("resultType") != "task"
        or not isinstance(identity, str)
        or not identity
    ):
        raise BindingError("mcp_result_unmeasured")
    return identity


def _task_result(
    result: dict[str, JsonValue], identity: str
) -> dict[str, JsonValue] | None:
    if result.get("taskId") != identity or result.get("resultType") != "complete":
        raise BindingError("mcp_task_identity")
    status = result.get("status")
    if status == "completed":
        value = result.get("result")
        if not isinstance(value, dict) or value.get("resultType") != "complete":
            raise BindingError("mcp_task_result_unmeasured")
        return value
    if status == "working":
        return None
    if status in ("failed", "cancelled", "input_required"):
        raise BindingError("mcp_task_" + str(status))
    raise BindingError("mcp_task_status_unmeasured")


def _poll_delay(result: dict[str, JsonValue], remaining: float) -> float:
    hint = result.get("pollIntervalMs", 50)
    if type(hint) is not int or hint < 0:
        raise BindingError("mcp_task_poll_interval")
    return min(max(hint / 1000, 0.05), max(remaining, 0))


class McpClient:
    def __init__(self, client: HarnClient, path: str = "/mcp") -> None:
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("MCP path must start with one slash")
        self.client, self.path = client, path
        self._discovered = False
        self._discovery_lock = threading.Lock()

    def rpc(self, method: str, params: dict[str, JsonValue]) -> dict[str, JsonValue]:
        identity = uuid.uuid4().hex
        raw = self.client._request(
            "POST",
            self.path,
            json=_body(method, params, identity),
            auth=method != facts.MCP_METHOD_SERVER_DISCOVER,
            protocol=False,
            mcp_headers=McpHeaders.for_request(method, params),
        )
        try:
            result = response_result(raw, identity, method)
            if not isinstance(result, dict):
                raise BindingError("mcp_response_not_object", method)
            return result
        except ValidationError:
            raise BindingError("mcp_response_malformed", method) from None

    def discover(self) -> None:
        with self._discovery_lock:
            if not self._discovered:
                discovery_result(self.rpc(facts.MCP_METHOD_SERVER_DISCOVER, {}))
                self._discovered = True

    def call(self, name: str, arguments: JsonValue) -> dict[str, JsonValue]:
        self.discover()
        result = self.rpc(
            facts.MCP_METHOD_TOOLS_CALL, {"name": name, "arguments": arguments}
        )
        identity = _task_identity(result)
        if identity is None:
            return result
        deadline = time.monotonic() + self.client.timeout
        while time.monotonic() < deadline:
            polled = self.rpc(facts.MCP_METHOD_TASKS_GET, {"taskId": identity})
            completed = _task_result(polled, identity)
            if completed is not None:
                return completed
            time.sleep(_poll_delay(polled, deadline - time.monotonic()))
        self.rpc(facts.MCP_METHOD_TASKS_CANCEL, {"taskId": identity})
        raise BindingError("mcp_task_timeout", name)


class AsyncMcpClient:
    def __init__(self, client: AsyncHarnClient, path: str = "/mcp") -> None:
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("MCP path must start with one slash")
        self.client, self.path = client, path
        self._discovered = False
        self._discovery_lock = asyncio.Lock()

    async def rpc(
        self,
        method: str,
        params: dict[str, JsonValue],
        *,
        identity: str | None = None,
    ) -> dict[str, JsonValue]:
        identity = identity or uuid.uuid4().hex
        raw = await self.client._request(
            "POST",
            self.path,
            json=_body(method, params, identity),
            auth=method != facts.MCP_METHOD_SERVER_DISCOVER,
            protocol=False,
            mcp_headers=McpHeaders.for_request(method, params),
        )
        try:
            result = response_result(raw, identity, method)
            if not isinstance(result, dict):
                raise BindingError("mcp_response_not_object", method)
            return result
        except ValidationError:
            raise BindingError("mcp_response_malformed", method) from None

    async def discover(self) -> None:
        async with self._discovery_lock:
            if not self._discovered:
                discovery_result(await self.rpc(facts.MCP_METHOD_SERVER_DISCOVER, {}))
                self._discovered = True

    async def _cancel(self, task_id: str) -> None:
        await self.rpc(facts.MCP_METHOD_TASKS_CANCEL, {"taskId": task_id})

    async def call(self, name: str, arguments: JsonValue) -> dict[str, JsonValue]:
        await self.discover()
        request_id, task_id = uuid.uuid4().hex, None
        try:
            result = await self.rpc(
                facts.MCP_METHOD_TOOLS_CALL,
                {"name": name, "arguments": arguments},
                identity=request_id,
            )
            task_id = _task_identity(result)
            if task_id is None:
                return result
            deadline = time.monotonic() + self.client.timeout
            while time.monotonic() < deadline:
                polled = await self.rpc(facts.MCP_METHOD_TASKS_GET, {"taskId": task_id})
                completed = _task_result(polled, task_id)
                if completed is not None:
                    return completed
                await asyncio.sleep(_poll_delay(polled, deadline - time.monotonic()))
            await self._cancel(task_id)
            raise BindingError("mcp_task_timeout", name)
        except asyncio.CancelledError as cancelled:
            # Cancelling the HTTP exchange closes its response stream. Only a
            # separately created task needs a cancellation request of its own.
            if task_id is not None:
                try:
                    await self._cancel(task_id)
                except Exception as delivery_error:
                    cancelled.add_note("MCP cancellation delivery was not acknowledged")
                    raise cancelled from delivery_error
            raise
