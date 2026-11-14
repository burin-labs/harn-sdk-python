"""Instance-owned native bindings on the official MCP protocol server."""

from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence

import anyio
from mcp import types
from mcp.server import Server, ServerRequestContext
from mcp.server.context import CallNext, HandlerResult
from mcp.shared.exceptions import MCPError
from pydantic import JsonValue, TypeAdapter

from ._binding_runtime import AsyncBinding, SyncBinding
from ._codegen.native import (
    CodegenCancellation,
    CodegenIdentity,
    NativeMcpBindingProfile,
    NativeMcpBindingVersion,
    NativeMcpOperationBinding,
    ToolCatalogSchemaVersion,
)
from ._codegen.protocol import MCP_METHOD_TOOLS_LIST
from ._mcp_stdio import stdio_transport
from .bindings import BindingError


def require_handlers(handlers: Mapping[str, object], names: Sequence[str]) -> None:
    if (
        not isinstance(handlers, Mapping)
        or set(handlers) != set(names)
        or any(not callable(handler) for handler in handlers.values())
    ):
        raise BindingError("native_handler_census")


class NativeServer:
    """One MCP stdio service per worker process."""

    def __init__(
        self,
        bindings: Sequence[SyncBinding | AsyncBinding],
        tools: Sequence[JsonValue],
        identity: Mapping[str, str],
        *,
        max_concurrency: int = 1,
    ) -> None:
        if not bindings or type(max_concurrency) is not int or max_concurrency < 1:
            raise BindingError("native_registration_unmeasured")
        self._bindings = {binding.name: binding for binding in bindings}
        if len(self._bindings) != len(bindings) or len(
            {binding.operation_id for binding in bindings}
        ) != len(bindings):
            raise BindingError("duplicate_native_registration")
        self._opaque_tools = copy.deepcopy(list(tools))
        self._tools = [types.Tool.model_validate(tool) for tool in self._opaque_tools]
        if len(self._tools) != len(bindings) or {
            tool.name for tool in self._tools
        } != set(self._bindings):
            raise BindingError("native_tool_census")
        self._profile = NativeMcpBindingProfile(
            schema_version=NativeMcpBindingVersion.HARN_TOOLS_MCP_1_0,
            catalog_schema_version=ToolCatalogSchemaVersion.HARN_TOOLS_2_0,
            identity=CodegenIdentity.model_validate(identity),
            operations=[
                NativeMcpOperationBinding(
                    name=binding.name, operation_id=binding.operation_id
                )
                for binding in bindings
            ],
            max_concurrency=max_concurrency,
            cancellation=CodegenCancellation.MCP_REQUEST,
        )
        self._limit = anyio.CapacityLimiter(max_concurrency)
        self._server = Server(
            "harn-native-python", on_list_tools=self._list, on_call_tool=self._call
        )
        self._server.middleware.append(self._project_tools)

    async def _project_tools(
        self, ctx: ServerRequestContext, call_next: CallNext
    ) -> HandlerResult:
        result = await call_next(ctx)
        if ctx.request_id is None or ctx.method != MCP_METHOD_TOOLS_LIST:
            return result
        if not isinstance(result, dict) or not isinstance(result.get("tools"), list):
            raise MCPError(types.INTERNAL_ERROR, "Native tool projection is unmeasured")
        projected = TypeAdapter(dict[str, JsonValue]).validate_python(
            result, strict=True
        )
        tools = projected["tools"]
        names = (
            [tool.get("name") if isinstance(tool, dict) else None for tool in tools]
            if isinstance(tools, list)
            else []
        )
        if (
            len(names) != len(self._tools)
            or any(not isinstance(name, str) for name in names)
            or set(names) != {tool.name for tool in self._tools}
        ):
            raise MCPError(
                types.INTERNAL_ERROR, "Native tool projection census differs"
            )
        # The SDK's spec-method sieve has already run. Forward Harn's opaque
        # catalog here so it cannot drop extensions or explicit null values.
        projected["tools"] = copy.deepcopy(self._opaque_tools)
        return projected

    async def _list(
        self,
        _context: ServerRequestContext,
        _params: types.PaginatedRequestParams | None,
    ) -> types.ListToolsResult:
        return types.ListToolsResult(tools=self._tools)

    async def _call(
        self, _context: ServerRequestContext, params: types.CallToolRequestParams
    ) -> types.CallToolResult:
        binding = self._bindings.get(params.name)
        if binding is None:
            raise MCPError(types.INVALID_PARAMS, "Unknown native tool")
        try:
            async with self._limit:
                arguments = params.arguments if params.arguments is not None else {}
                if isinstance(binding, AsyncBinding):
                    result = await binding.invoke(arguments)
                else:
                    result = await anyio.to_thread.run_sync(binding.invoke, arguments)
                return types.CallToolResult.model_validate(result)
        except BindingError as error:
            code = (
                types.INVALID_PARAMS
                if error.code == "invalid_wire_value"
                else types.INTERNAL_ERROR
            )
            raise MCPError(
                code,
                "Native binding refused the value",
                {"operation": binding.operation_id, "kind": error.code},
            ) from None
        except Exception:  # noqa: BLE001 - user exceptions cross as value-free runtime faults.
            raise MCPError(
                types.INTERNAL_ERROR,
                "Native handler failed",
                {"operation": binding.operation_id, "kind": "runtime_fault"},
            ) from None

    async def _serve_stdio(self) -> None:
        async with stdio_transport(self._profile.model_dump(mode="json")) as (
            read,
            write,
        ):
            await self._server.run(
                read, write, self._server.create_initialization_options()
            )

    def run_stdio(self) -> None:
        anyio.run(self._serve_stdio)
