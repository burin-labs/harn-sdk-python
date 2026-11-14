"""Real subprocess fixture; the generated factory owns registration and codecs."""

import asyncio
import importlib.util
import json
import sys
from pathlib import Path

from harn.bindings import ApplicationFailure

path = Path(sys.argv[1])
root = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("bindings", path)
assert spec is not None and spec.loader is not None
bindings = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = bindings
spec.loader.exec_module(bindings)
if len(sys.argv) > 3 and sys.argv[3] == "opaque":
    tools = json.loads(bindings._MCP_TOOLS_JSON)
    tools[0]["futureExtension"] = {"opaque": None}
    tools[0]["description"] = None
    bindings._MCP_TOOLS_JSON = json.dumps(tools)


async def echo(arguments):
    print("handler-output-is-not-protocol")
    return arguments.input


async def mutate(arguments):
    (root / "reached").write_text("reached")
    print("fixture-reached", file=sys.stderr, flush=True)
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        # Even handled cancellation must not publish a late result.
        return arguments.input
    finally:
        (root / "stopped").write_text("stopped")
        print("fixture-stopped", file=sys.stderr, flush=True)


async def reject(_arguments):
    return ApplicationFailure(
        error=bindings.Failure_Rejected(
            enum_name="Failure", variant="Rejected", fields=("rejected",)
        )
    )


bindings.create_async_server(
    {"echo": echo, "mutate": mutate, "reject": reject, "scheduled": echo},
    max_concurrency=2,
).run_stdio()
