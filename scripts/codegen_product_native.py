"""Real native-worker projections and recorded-identity cleanup for the product gate."""

from __future__ import annotations

import asyncio
import errno
import json
import math
import os
import queue
import re
import select
import shutil
import signal
import subprocess
import sys
import threading
import time
from contextlib import contextmanager, suppress
from pathlib import Path

from pydantic import TypeAdapter

from harn import AsyncHarnClient
from harn._wire_json import loads
from harn.bindings import ApplicationFailure, BindingError, parse_wire_json


def _current(pid: int):
    try:
        return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    except FileNotFoundError:
        return None


def _reaped(identity):
    current = _current(identity["pid"])
    if current is not None and current[19] == identity["start"]:
        try:
            descriptor = os.pidfd_open(identity["pid"])
        except ProcessLookupError:
            descriptor = None
        if descriptor is not None:
            try:
                current = _current(identity["pid"])
                if current is None or current[19] != identity["start"]:
                    return
                poll = select.poll()
                deadline = time.monotonic() + 30
                poll.register(descriptor, select.POLLIN)
                events = poll.poll(30000)
                current = _current(identity["pid"])
                if current is None or current[19] != identity["start"]:
                    return
                if any(flags & select.POLLIN for _, flags in events):
                    remaining = max(0, math.ceil((deadline - time.monotonic()) * 1000))
                    poll.modify(descriptor, select.POLLHUP)
                    # Older kernels lack HUP; the final birth-identity read
                    # still decides whether reaping actually completed.
                    poll.poll(remaining)
            finally:
                os.close(descriptor)
    current = _current(identity["pid"])
    assert current is None or current[19] != identity["start"], (
        "Recorded worker is not reaped",
        identity,
    )


@contextmanager
def _server(executable, source, cohort, environment):
    child = subprocess.Popen(
        [
            executable,
            "serve",
            "mcp",
            "--surface",
            "script",
            "--transport",
            "http",
            "--bind",
            "127.0.0.1:0",
            "--obs",
            "off",
            str(source),
        ],
        cwd=cohort,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    ready, logs = queue.Queue(), []

    def read():
        for line in child.stderr:
            logs.append(line)
            match = re.search(
                r"MCP workflow server ready on (http://127\.0\.0\.1:[0-9]+)/mcp", line
            )
            if match:
                ready.put(match.group(1))

    reader = threading.Thread(target=read)
    reader.start()
    try:
        yield ready.get(timeout=30)
    finally:
        if child.poll() is None:
            child.send_signal(signal.SIGINT)
        try:
            try:
                child.wait(timeout=30)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=30)
                raise AssertionError(
                    "Recorded Harn server did not stop after SIGINT"
                ) from None
        finally:
            reader.join(timeout=30)
            assert not reader.is_alive()
            (cohort / "harn.log").write_text("".join(logs))


def qualify_native(executable, scratch, fixture_root, generated, module, payload):
    assert sys.platform == "linux", (
        "Native product qualification requires Linux process identities"
    )
    expected = loads(payload)
    arguments = parse_wire_json(
        TypeAdapter(module.EchoInput), '{"input":' + payload + "}"
    )
    completed = []
    for mode in ("cli", "normal", "malformed", "cancel", "stderr"):
        cohort = scratch / ("native-" + mode)
        cohort.mkdir()
        source, worker = cohort / "native.harn", cohort / "worker.py"
        shutil.copyfile(fixture_root / "native_registry.harn", source)
        shutil.copyfile(fixture_root / "native_worker.py", worker)
        shutil.copyfile(generated, cohort / "bindings.py")
        shutil.copyfile(scratch / "source/ir.json", cohort / "ir.json")
        spec = {
            "program": sys.executable,
            "args": [
                str(cohort / "bindings.py"),
                str(cohort),
                "normal" if mode == "cli" else mode,
            ],
            "cwd": str(cohort),
            "environment": {
                "PATH": str(Path(sys.executable).parent) + os.pathsep + os.defpath,
                "HOME": str(cohort),
            },
        }
        spec["args"].insert(0, str(worker))
        environment = {
            **spec["environment"],
            "LANG": "C.UTF-8",
            "HARN_EXT_NATIVE_FIXTURE": json.dumps(
                {"ir": str(cohort / "ir.json"), "process": spec}
            ),
        }
        if mode == "cli":
            inputs = cohort / "arguments.json"
            inputs.write_text('{"input":' + payload + "}")
            result = subprocess.run(
                [
                    executable,
                    "tool",
                    "run",
                    str(source),
                    "echo",
                    "--harn-input",
                    "@" + str(inputs),
                    "--harn-output",
                    "json",
                ],
                cwd=cohort,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
                timeout=90,
            )
            (cohort / "harn.stderr").write_text(result.stderr)
            assert result.returncode == 0, result.stderr
            assert loads(result.stdout) == expected
            calls = [
                json.loads(line)
                for line in (cohort / "calls.ndjson").read_text().splitlines()
            ]
            assert len(calls) == 1 and calls[0]["operation"] == "echo"
        else:
            eventfd = None
            if mode == "cancel":
                os.mkfifo(cohort / "events.fifo")
                os.mkfifo(cohort / "release.fifo")
                eventfd = os.open(cohort / "events.fifo", os.O_RDWR | os.O_NONBLOCK)
            try:
                with _server(executable, source, cohort, environment) as base_url:

                    async def run(
                        mode=mode, cohort=cohort, eventfd=eventfd, base_url=base_url
                    ):
                        async with AsyncHarnClient(
                            base_url=base_url, timeout=90
                        ) as transport:
                            client = module.AsyncClient(transport)
                            adapter = TypeAdapter(module.Payload)
                            if mode == "malformed":
                                try:
                                    await client.echo(arguments)
                                except BindingError as error:
                                    assert error.code == "tool_runtime_failure"
                                else:
                                    raise AssertionError(
                                        "Malformed worker output became success"
                                    )
                                calls = [
                                    json.loads(line)
                                    for line in (cohort / "calls.ndjson")
                                    .read_text()
                                    .splitlines()
                                ]
                                assert (
                                    len(calls) == 1
                                    and calls[0]["kind"] == "malformed-output"
                                )
                                return
                            assert (
                                loads(
                                    adapter.dump_json(
                                        await client.echo(arguments),
                                        by_alias=True,
                                        exclude_unset=True,
                                    )
                                )
                                == expected
                            )
                            if mode == "normal":
                                failure = await client.reject(arguments)
                                assert (
                                    isinstance(failure, ApplicationFailure)
                                    and failure.error.variant == "Rejected"
                                )
                                assert (
                                    loads(
                                        adapter.dump_json(
                                            await client.scheduled(arguments),
                                            by_alias=True,
                                            exclude_unset=True,
                                        )
                                    )
                                    == expected
                                )
                            elif mode == "stderr":
                                for _ in range(2):
                                    assert (
                                        loads(
                                            adapter.dump_json(
                                                await client.echo(arguments),
                                                by_alias=True,
                                                exclude_unset=True,
                                            )
                                        )
                                        == expected
                                    )
                                writes = [
                                    json.loads(line)
                                    for line in (cohort / "stderr.ndjson")
                                    .read_text()
                                    .splitlines()
                                ]
                                assert (
                                    len(writes) == 3
                                    and writes[1]["written"]
                                    > writes[1]["capacity"] + 65536
                                )
                            else:
                                events, buffer = asyncio.Queue(), b""

                                def read_events():
                                    nonlocal buffer
                                    buffer += os.read(eventfd, 65536)
                                    while b"\n" in buffer:
                                        line, buffer = buffer.split(b"\n", 1)
                                        events.put_nowait(json.loads(line))

                                loop = asyncio.get_running_loop()
                                loop.add_reader(eventfd, read_events)

                                async def milestone(kind):
                                    while True:
                                        event = await events.get()
                                        if (
                                            event["operation"] == "mutate"
                                            and event["kind"] == kind
                                        ):
                                            return event

                                waiting = asyncio.create_task(client.mutate(arguments))
                                try:
                                    await asyncio.wait_for(milestone("parked"), 30)
                                    waiting.cancel()
                                    try:
                                        await waiting
                                    except asyncio.CancelledError:
                                        pass
                                    else:
                                        raise AssertionError(
                                            "Async HTTP exchange was not canceled"
                                        )
                                    # A watchdog bounds a never-expiring fixture, not a latency target.
                                    value, _ = await asyncio.wait_for(
                                        asyncio.gather(
                                            client.echo(arguments), milestone("stopped")
                                        ),
                                        30,
                                    )
                                    assert value.sequence == 9223372036854775807
                                    calls = [
                                        json.loads(line)
                                        for line in (cohort / "calls.ndjson")
                                        .read_text()
                                        .splitlines()
                                    ]
                                    events_seen = [
                                        call["kind"]
                                        for call in calls
                                        if call["operation"] == "mutate"
                                    ]
                                    assert (
                                        "cancelled" in events_seen
                                        and "continued" not in events_seen
                                    )
                                finally:
                                    # On a regression, release only the known fixture so cleanup can finish.
                                    try:
                                        descriptor = os.open(
                                            cohort / "release.fifo",
                                            os.O_WRONLY | os.O_NONBLOCK,
                                        )
                                    except OSError as error:
                                        if error.errno != errno.ENXIO:
                                            raise
                                    else:
                                        os.write(descriptor, b"release\n")
                                        os.close(descriptor)
                                    if not waiting.done():
                                        waiting.cancel()
                                    with suppress(asyncio.CancelledError):
                                        await waiting
                                    loop.remove_reader(eventfd)

                    asyncio.run(run())
            finally:
                if eventfd is not None:
                    os.close(eventfd)
        identity = json.loads((cohort / "worker.json").read_text())
        _reaped(identity)
        completed.append({"mode": mode, "recorded_worker_reaped": identity})
    assert len(completed) == 5
    return {"cohorts": completed, "global_census_claimed": False, "pending": 0}
