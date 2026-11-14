"""Small frame budget exercises the unchanged production framing actor."""

import sys
from pathlib import Path

from mcp.server.stdio import stdio_server

from harn import _mcp_stdio
from harn._binding_runtime import AsyncBinding
from harn._mcp_server import NativeServer

root = Path(sys.argv[1])
_mcp_stdio.MCP_MAX_STDIO_LINE_BYTES = 4096


async def invoke(arguments):
    with (root / "called").open("a") as output:
        output.write("called\n")
    if arguments.get("claim_again"):
        try:
            async with stdio_server():
                raise AssertionError("Official stdio owner allowed a second claim")
        except RuntimeError as error:
            assert "already claimed" in str(error)
    value = "x" * 5000 if arguments.get("large_output") else "okay"
    return {
        "resultType": "complete",
        "isError": False,
        "content": [],
        "structuredContent": {"value": value},
    }


NativeServer(
    [AsyncBinding("operation:measured", "measured", invoke)],
    [{"name": "measured", "inputSchema": {"type": "object"}}],
    dict.fromkeys(["catalog_digest", "binding_digest", "ir_digest"], "a" * 64),
).run_stdio()
