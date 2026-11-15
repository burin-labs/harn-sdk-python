"""Instrument generated handlers; malformed mode deliberately bypasses its codec."""

import asyncio
import importlib.util
import json
import os
import sys
from pathlib import Path

from harn._binding_runtime import AsyncBinding
from harn.bindings import ApplicationFailure

path, directory, mode = sys.argv[1:]
root = Path(directory)
spec = importlib.util.spec_from_file_location("native_fixture_bindings", path)
assert spec is not None and spec.loader is not None
bindings = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = bindings
spec.loader.exec_module(bindings)
identity = {
    "pid": os.getpid(),
    "start": Path("/proc/self/stat").read_text().rsplit(")", 1)[1].split()[19],
}
(root / "worker.json").write_text(json.dumps(identity))


def event(kind, operation):
    record = {**identity, "kind": kind, "operation": operation}
    with (root / "calls.ndjson").open("a") as stream:
        stream.write(json.dumps(record) + "\n")
    if (root / "events.fifo").exists():
        with (root / "events.fifo").open("w") as stream:
            stream.write(json.dumps(record) + "\n")


async def release():
    descriptor = os.open(root / "release.fifo", os.O_RDWR | os.O_NONBLOCK)
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    def ready():
        if os.read(descriptor, 4096) and not future.done():
            future.set_result(None)

    loop.add_reader(descriptor, ready)
    event("parked", "mutate")
    try:
        await future
    finally:
        loop.remove_reader(descriptor)
        os.close(descriptor)


calls = 0


async def echo(arguments):
    global calls
    calls += 1
    event("reached", "echo")
    if mode == "stderr":
        import fcntl

        capacity = fcntl.fcntl(2, fcntl.F_GETPIPE_SZ)
        assert 0 < capacity <= 16777216
        size = capacity + 65537 if calls == 2 else 512
        data = b"x" * size
        written = 0
        while written < size:
            count = os.write(2, data[written:])
            assert count > 0
            written += count
        with (root / "stderr.ndjson").open("a") as stream:
            stream.write(json.dumps({"written": written, "capacity": capacity}) + "\n")
    return arguments.input


async def mutate(arguments):
    event("reached", "mutate")
    if mode == "cancel":
        try:
            await release()
            event("continued", "mutate")
        except asyncio.CancelledError:
            event("cancelled", "mutate")
            raise
        finally:
            event("stopped", "mutate")
    return arguments.input


async def reject(_arguments):
    event("reached", "reject")
    return ApplicationFailure(
        error=bindings.Failure_Rejected(
            enum_name="Failure", variant="Rejected", fields=("rejected",)
        )
    )


async def scheduled(arguments):
    event("reached", "scheduled")
    return arguments.input


server = bindings.create_async_server(
    {"echo": echo, "mutate": mutate, "reject": reject, "scheduled": scheduled},
    max_concurrency=2,
)
if mode == "malformed":
    original = server._bindings["echo"]

    async def malformed(_arguments):
        event("malformed-output", "echo")
        return {
            "resultType": "complete",
            "isError": False,
            "content": [],
            "structuredContent": {"invalid": True},
        }

    server._bindings["echo"] = AsyncBinding(
        original.operation_id, original.name, malformed
    )
server.run_stdio()
