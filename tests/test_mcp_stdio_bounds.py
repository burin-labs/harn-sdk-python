"""Bounded pipes include non-null dispatch and blocked-reader teardown controls."""

import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from harn._mcp_protocol import request_params
from harn._mcp_stdio_claim import check_stdio_api


def test_private_owner_version_and_api_are_measured_before_any_claim(monkeypatch):
    from harn import _mcp_stdio_claim

    check_stdio_api()
    monkeypatch.setattr(_mcp_stdio_claim, "version", lambda _name: "unknown")
    with pytest.raises(RuntimeError, match="ownership version"):
        check_stdio_api()
    monkeypatch.setattr(_mcp_stdio_claim, "version", lambda _name: "2.3.0")
    called = []

    def invalid_claim(unknown):
        called.append(unknown)

    monkeypatch.setattr(_mcp_stdio_claim.stdio, "_claim_fd", invalid_claim)
    with pytest.raises(RuntimeError, match="ownership API"):
        check_stdio_api()
    assert called == []


@pytest.mark.parametrize("outgoing", [False, True])
def test_exact_utf8_frame_bound_then_refusal_terminates_with_stdin_still_open(
    tmp_path, outgoing
):
    fixture = Path(__file__).parent / "fixtures/codegen/frame_worker.py"
    environment = {
        "PATH": os.environ["PATH"],
        "HOME": str(tmp_path),
        "PYTHONPATH": str(Path(__file__).parents[1] / "src"),
    }
    child = subprocess.Popen(
        [sys.executable, str(fixture), str(tmp_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
    )
    responses = queue.Queue()
    errors = []

    def read_output():
        for line in child.stdout:
            responses.put(json.loads(line))

    def read_errors():
        errors.append(child.stderr.read())

    readers = [
        threading.Thread(target=read_output),
        threading.Thread(target=read_errors),
    ]
    for reader in readers:
        reader.start()

    def frame(identity, arguments, size=None):
        message = {
            "jsonrpc": "2.0",
            "id": identity,
            "method": "tools/call",
            "params": request_params({"name": "measured", "arguments": arguments}),
        }
        if size is not None:
            message["params"]["arguments"]["padding"] = ""
            empty = json.dumps(message, ensure_ascii=False).encode() + b"\n"
            assert size >= len(empty)
            message["params"]["arguments"]["padding"] = "x" * (size - len(empty))
        encoded = json.dumps(message, ensure_ascii=False).encode() + b"\n"
        assert size is None or len(encoded) == size
        return encoded

    try:
        child.stdin.write(frame("positive", {"snow": "雪", "claim_again": True}, 4096))
        child.stdin.flush()
        positive = responses.get(timeout=30)
        assert positive["id"] == "positive" and positive["result"][
            "structuredContent"
        ] == {"value": "okay"}
        assert (tmp_path / "called").read_text().splitlines() == ["called"]
        child.stdin.write(
            frame(
                "refused",
                {"large_output": True} if outgoing else {"snow": "雪"},
                None if outgoing else 4097,
            )
        )
        child.stdin.flush()
        # The input pipe stays open: an output refusal must cancel a blocked reader.
        assert child.wait(timeout=30) != 0
        for reader in readers:
            reader.join(timeout=30)
            assert not reader.is_alive()
        assert responses.empty(), "No partial or oversized response may be published"
        assert len((tmp_path / "called").read_text().splitlines()) == (
            2 if outgoing else 1
        )
        assert b"mcp_frame_too_large" in b"".join(errors)
    finally:
        if child.poll() is None:
            child.terminate()
            child.wait(timeout=30)
        child.stdin.close()
        for reader in readers:
            reader.join(timeout=30)


def test_unterminated_final_segment_never_reaches_a_handler(tmp_path):
    fixture = Path(__file__).parent / "fixtures/codegen/frame_worker.py"
    child = subprocess.Popen(
        [sys.executable, str(fixture), str(tmp_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            "PATH": os.environ["PATH"],
            "HOME": str(tmp_path),
            "PYTHONPATH": str(Path(__file__).parents[1] / "src"),
        },
    )

    def encoded(identity):
        return json.dumps(
            {
                "jsonrpc": "2.0",
                "id": identity,
                "method": "tools/call",
                "params": request_params({"name": "measured", "arguments": {}}),
            }
        ).encode()

    try:
        child.stdin.write(encoded("positive") + b"\n")
        child.stdin.flush()
        assert json.loads(child.stdout.readline())["id"] == "positive"
        assert (tmp_path / "called").read_text().splitlines() == ["called"]
        child.stdin.write(encoded("unterminated"))
        child.stdin.close()
        assert child.wait(timeout=30) != 0
        assert child.stdout.read() == b""
        assert (tmp_path / "called").read_text().splitlines() == ["called"]
        assert b"mcp_unterminated_frame" in child.stderr.read()
    finally:
        if child.poll() is None:
            child.terminate()
            child.wait(timeout=30)
