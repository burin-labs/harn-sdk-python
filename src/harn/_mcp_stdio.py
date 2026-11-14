"""Lossless NDJSON framing; the official MCP Server owns protocol and cancellation."""

from __future__ import annotations

import threading
from collections.abc import AsyncIterator
from concurrent.futures import CancelledError
from contextlib import asynccontextmanager, suppress
from typing import BinaryIO

import anyio
from anyio.from_thread import BlockingPortal
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from mcp import types
from mcp.shared.message import SessionMessage
from pydantic import JsonValue

from ._codegen.protocol import HARN_NATIVE_BINDING_META_KEY, MCP_MAX_STDIO_LINE_BYTES
from ._mcp_stdio_claim import claim_stdio
from ._wire_json import loads
from .bindings import BindingError


@asynccontextmanager
async def input_lines(
    stream: BinaryIO,
) -> AsyncIterator[MemoryObjectReceiveStream[bytes | BindingError]]:
    sender, receiver = anyio.create_memory_object_stream[bytes | BindingError](0)
    async with BlockingPortal() as portal:

        def read() -> None:
            try:
                while line := stream.readline(MCP_MAX_STDIO_LINE_BYTES + 1):
                    portal.call(sender.send, line)
            except (OSError, ValueError):
                with suppress(RuntimeError, CancelledError, anyio.BrokenResourceError):
                    portal.call(sender.send, BindingError("mcp_input_failed"))
            except (RuntimeError, CancelledError, anyio.BrokenResourceError):
                pass
            finally:
                with suppress(RuntimeError, CancelledError, anyio.BrokenResourceError):
                    portal.call(sender.aclose)

        # A blocked read cannot be canceled portably. The SDK retains its
        # descriptor, and this daemon must not prevent a failed worker exiting.
        threading.Thread(target=read, name="Harn MCP input", daemon=True).start()
        try:
            yield receiver
        finally:
            receiver.close()


@asynccontextmanager
async def stdio_transport(
    profile: dict[str, JsonValue],
) -> AsyncIterator[
    tuple[
        MemoryObjectReceiveStream[SessionMessage | Exception],
        MemoryObjectSendStream[SessionMessage],
    ]
]:
    with claim_stdio() as (input_file, output_file):
        writer = anyio.wrap_file(output_file)
        incoming_writer, incoming = anyio.create_memory_object_stream[
            SessionMessage | Exception
        ](0)
        outgoing, outgoing_reader = anyio.create_memory_object_stream[SessionMessage](0)

        async def read() -> None:
            async with incoming_writer, input_lines(input_file) as lines:
                async for line in lines:
                    if isinstance(line, BindingError):
                        raise line
                    if len(line) > MCP_MAX_STDIO_LINE_BYTES:
                        raise BindingError("mcp_frame_too_large")
                    if not line.endswith(b"\n"):
                        raise BindingError("mcp_unterminated_frame")
                    try:
                        message = types.jsonrpc_message_adapter.validate_python(
                            loads(line), strict=True, by_name=False
                        )
                    except (BindingError, ValueError, TypeError):
                        await incoming_writer.send(BindingError("mcp_invalid_json"))
                    else:
                        await incoming_writer.send(SessionMessage(message))

        async def write() -> None:
            async with outgoing_reader:
                async for item in outgoing_reader:
                    message = item.message
                    if isinstance(message, types.JSONRPCResponse):
                        result = dict(message.result)
                        metadata = dict(result.get("_meta") or {})
                        metadata[HARN_NATIVE_BINDING_META_KEY] = profile
                        result["_meta"] = metadata
                        message = message.model_copy(update={"result": result})
                    encoded = (
                        message.model_dump_json(by_alias=True, exclude_unset=True)
                        + "\n"
                    ).encode("utf-8")
                    if len(encoded) > MCP_MAX_STDIO_LINE_BYTES:
                        raise BindingError("mcp_frame_too_large")
                    await writer.write(encoded)
                    await writer.flush()

        async with anyio.create_task_group() as tasks:
            tasks.start_soon(read)
            tasks.start_soon(write)
            try:
                yield incoming, outgoing
            finally:
                tasks.cancel_scope.cancel()
