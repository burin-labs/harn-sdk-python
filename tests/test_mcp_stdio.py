"""Real pipes through the official MCP protocol owner and generated handlers."""

import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from harn._codegen.api import render
from harn._codegen.protocol import (
    HARN_MCP_TOOL_CONTRACT_META_KEY,
    HARN_NATIVE_BINDING_META_KEY,
)
from harn._codegen.request import CodegenIr, CodegenRole
from harn._mcp_protocol import request_params
from harn._wire_json import loads
from harn.bindings import BindingError

FIXTURE = Path(__file__).parent / "fixtures/codegen"


@pytest.mark.parametrize("opaque_extensions", [False, True])
def test_real_stdio_catalog_exact_values_cancellation_and_output_isolation(
    tmp_path, opaque_extensions
):
    ir = CodegenIr.model_validate_json((FIXTURE / "pathological/ir.json").read_bytes())
    artifact = render(ir, CodegenRole.BOTH)
    path = tmp_path / artifact.path
    path.write_text(artifact.content)
    if opaque_extensions:
        ir.mcp_tools[0]["futureExtension"] = {"opaque": None}
        ir.mcp_tools[0]["description"] = None
    payload = (FIXTURE / "pathological/input.json").read_text().strip()
    expected = loads(payload)
    environment = {
        "PATH": os.environ["PATH"],
        "HOME": str(tmp_path),
        "PYTHONPATH": str(Path(__file__).parents[1] / "src"),
        **(
            {"SYSTEMROOT": os.environ["SYSTEMROOT"]}
            if "SYSTEMROOT" in os.environ
            else {}
        ),
    }
    child = subprocess.Popen(
        [
            sys.executable,
            str(FIXTURE / "stdio_worker.py"),
            str(path),
            str(tmp_path),
            "opaque" if opaque_extensions else "original",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=environment,
    )
    responses, events = queue.Queue(), queue.Queue()
    errors = []

    def read_output():
        for line in child.stdout:
            try:
                responses.put(loads(line))
            except BindingError as error:
                responses.put(error)

    def read_errors():
        for line in child.stderr:
            errors.append(line)
            if line.strip().startswith("fixture-"):
                events.put(line.strip())

    readers = [
        threading.Thread(target=read_output),
        threading.Thread(target=read_errors),
    ]
    for reader in readers:
        reader.start()

    def send(method, identity=None, params=None, *, arguments=False):
        frame = {
            "jsonrpc": "2.0",
            "method": method,
            "params": request_params(params or {}),
        }
        if identity is not None:
            frame["id"] = identity
        wire = json.dumps(frame)
        if arguments:
            wire = wire.replace(
                '"arguments": null', '"arguments":{"input":' + payload + "}"
            )
        child.stdin.write(wire + "\n")
        child.stdin.flush()

    def receive(identity):
        reply = responses.get(timeout=30)
        assert isinstance(reply, dict), reply
        assert reply.get("id") == identity, reply
        assert "error" not in reply, reply
        return reply["result"]

    try:
        send("server/discover", 9223372036854775807)
        profile = receive(9223372036854775807)["_meta"][HARN_NATIVE_BINDING_META_KEY]
        assert profile["identity"] == ir.identity.model_dump(mode="json")
        assert profile["max_concurrency"] == 2
        send("tools/list", "list")
        assert receive("list")["tools"] == ir.mcp_tools
        send("tools/call", "echo", {"name": "echo", "arguments": None}, arguments=True)
        value = receive("echo")["structuredContent"]
        assert value == expected
        assert type(value["floating"]) is float and type(value["sequence"]) is int
        assert value["sequence"] == 9223372036854775807 and value["scalars"] == [
            True,
            1,
        ]
        send(
            "tools/call",
            "reject",
            {"name": "reject", "arguments": None},
            arguments=True,
        )
        failure = receive("reject")
        assert failure["isError"] is True
        assert (
            failure["_meta"][HARN_MCP_TOOL_CONTRACT_META_KEY]["applicationError"][
                "data"
            ]["variant"]
            == "Rejected"
        )
        send(
            "tools/call",
            "cancel",
            {"name": "mutate", "arguments": None},
            arguments=True,
        )
        assert events.get(timeout=30) == "fixture-reached"
        assert (tmp_path / "reached").read_text() == "reached"
        send(
            "notifications/cancelled",
            params={"requestId": "cancel", "reason": "fixture"},
        )
        send("tools/call", "other", {"name": "echo", "arguments": None}, arguments=True)
        assert receive("other")["structuredContent"] == expected
        assert events.get(timeout=30) == "fixture-stopped"
        assert (tmp_path / "stopped").read_text() == "stopped"
        send("tools/list", "barrier")
        receive("barrier")
        child.stdin.close()
        assert child.wait(timeout=30) == 0
        for reader in readers:
            reader.join(timeout=30)
            assert not reader.is_alive()
        assert responses.empty(), (
            "No canceled response or handler print may reach stdout"
        )
        assert "handler-output-is-not-protocol" in "".join(errors)
    finally:
        if child.poll() is None:
            child.terminate()
            child.wait(timeout=30)
        for reader in readers:
            reader.join(timeout=30)
