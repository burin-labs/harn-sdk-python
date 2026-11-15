"""Render typed invocation and registration over the normalized wire graph."""

from __future__ import annotations

import json

from .names import Symbol, allocate
from .render import ArtifactBuilder, render_types
from .request import CodegenIr, CodegenRole
from .response import GeneratedArtifact
from .types import RESERVED, TypeRenderer


def render(ir: CodegenIr, role: CodegenRole) -> GeneratedArtifact:
    renderer = TypeRenderer(ir)
    artifact = render_types(ir)
    builder = ArtifactBuilder()
    builder.append(artifact.content)
    builder.mappings.extend(artifact.source_mappings)
    operations = sorted(ir.operations, key=lambda operation: operation.id)
    names = allocate(
        (Symbol(operation.id, operation.name) for operation in operations),
        reserved=RESERVED | frozenset(renderer.names.values()) | {"self", "init"},
    )
    builder.append(
        "\nfrom collections.abc import Awaitable\n"
        "from typing import Protocol, TypedDict\n"
        "from pydantic import JsonValue, TypeAdapter\n"
        "from harn import HarnClient, AsyncHarnClient\n"
        "from harn._binding_runtime import bind_sync, bind_async, encode_wire, decode_result\n"
        "from harn._mcp_client import McpClient, AsyncMcpClient\n"
        "from harn._mcp_server import NativeServer, require_handlers\n\n"
    )
    builder.append("CATALOG_DIGEST = " + repr(ir.identity.catalog_digest) + "\n")
    builder.append("BINDING_DIGEST = " + repr(ir.identity.binding_digest) + "\n")
    builder.append("IR_DIGEST = " + repr(ir.identity.ir_digest) + "\n")
    adapters = {}
    for index, wire in enumerate(sorted(ir.types, key=lambda wire: wire.id)):
        name = renderer.reference(wire.id)
        adapters[wire.id] = f"_adapter_{index}"
        builder.append(f"_adapter_{index} = TypeAdapter[{name}]({name})\n")
        builder.append(f"_adapter_{index}.rebuild(_types_namespace=globals())\n")

    if role in (CodegenRole.CLIENT, CodegenRole.BOTH):
        for asynchronous in (False, True):
            client, transport, runtime = (
                ("AsyncClient", "AsyncHarnClient", "AsyncMcpClient")
                if asynchronous
                else ("Client", "HarnClient", "McpClient")
            )
            builder.append(f"\nclass {client}:\n")
            builder.append(
                f"    def __init__(self, client: {transport}, *, path: str = '/mcp') -> None:\n"
            )
            builder.append(f"        self._mcp = {runtime}(client, path)\n")
            for operation in operations:
                if operation.output.kind != "value":
                    raise ValueError("validated operation has no output")
                input_type = renderer.reference(operation.input)
                output_type = renderer.reference(operation.output.type_id)
                error_type = (
                    renderer.reference(operation.application_error)
                    if operation.application_error
                    else None
                )
                result_type = output_type + (
                    f" | ApplicationFailure[{error_type}]" if error_type else ""
                )
                error_adapter = (
                    adapters[operation.application_error]
                    if operation.application_error
                    else "None"
                )
                prefix, wait = ("async ", "await ") if asynchronous else ("", "")
                builder.append(
                    f"\n    {prefix}def {names[operation.id]}(self, arguments: {input_type}) -> {result_type}:\n"
                    f"        result = {wait}self._mcp.call({operation.name!r}, encode_wire({adapters[operation.input]}, arguments))\n"
                    f"        return decode_result({operation.name!r}, result, {adapters[operation.output.type_id]}, {error_adapter}, result_property={operation.output.mcp_envelope.value == 'result_property'})\n",
                    operation.source,
                )
    if role in (CodegenRole.SERVER, CodegenRole.BOTH):
        builder.append(
            f"\n_MCP_TOOLS_JSON = {json.dumps(ir.mcp_tools, separators=(',', ':'), ensure_ascii=True)!r}\n"
        )
        for asynchronous in (False, True):
            prefix = "Async" if asynchronous else "Sync"
            for index, operation in enumerate(operations):
                if operation.output.kind != "value":
                    raise ValueError("validated operation has no output")
                output_type = renderer.reference(operation.output.type_id)
                if operation.application_error:
                    output_type += f" | ApplicationFailure[{renderer.reference(operation.application_error)}]"
                result_type = (
                    f"Awaitable[{output_type}]" if asynchronous else output_type
                )
                builder.append(
                    f"\nclass _{prefix}Handler{index}(Protocol):\n"
                    f"    def __call__(self, arguments: {renderer.reference(operation.input)}, /) -> {result_type}: ...\n",
                    operation.source,
                )
            builder.append(f"\nclass {prefix}Handlers(TypedDict):\n")
            if not operations:
                builder.append("    pass\n")
            for index, operation in enumerate(operations):
                builder.append(f"    {names[operation.id]}: _{prefix}Handler{index}\n")
            factory = "create_async_server" if asynchronous else "create_server"
            bind = "bind_async" if asynchronous else "bind_sync"
            builder.append(
                f"\ndef {factory}(handlers: {prefix}Handlers, *, max_concurrency: int = 1) -> NativeServer:\n"
            )
            builder.append(
                f"    require_handlers(handlers, {list(names.values())!r})\n"
            )
            builder.append("    return NativeServer([\n")
            for operation in operations:
                assert operation.output.kind == "value"
                error_adapter = (
                    adapters[operation.application_error]
                    if operation.application_error
                    else "None"
                )
                builder.append(
                    f"        {bind}({operation.id!r}, {operation.name!r}, handlers[{names[operation.id]!r}], {adapters[operation.input]}, {adapters[operation.output.type_id]}, {error_adapter}, result_property={operation.output.mcp_envelope.value == 'result_property'}),\n"
                )
            builder.append(
                "    ], TypeAdapter(list[JsonValue]).validate_json(_MCP_TOOLS_JSON), "
                f"{ir.identity.model_dump(mode='json')!r}, max_concurrency=max_concurrency)\n"
            )
    return builder.artifact()
