"""Qualify an installed wheel against a real Harn source contract and HTTP server."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
import queue
import re
import shutil
import signal
import subprocess
import sys
import sysconfig
import tempfile
import threading
from importlib.metadata import version
from pathlib import Path

import httpx
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

import harn
from harn import AsyncHarnClient, HarnClient
from harn._codegen import protocol as facts
from harn._codegen.diagnostic import CodegenDiagnostic
from harn._wire_json import loads
from harn.bindings import ApplicationFailure

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harn", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    args.receipt.write_text(
        json.dumps({"status": "running", "pending": 1, "failing_names": []}) + "\n"
    )
    executable = shutil.which(args.harn)
    backend = shutil.which("harn-codegen-python", path=sysconfig.get_path("scripts"))
    assert executable is not None and backend is not None
    assert not Path(harn.__file__).resolve().is_relative_to(ROOT / "src")
    scratch = Path(tempfile.mkdtemp(prefix="harn-python-product-"))
    fixture = scratch / "source"
    shutil.copytree(ROOT / "tests/fixtures/codegen/pathological", fixture)
    home = scratch / "home"
    home.mkdir()
    environment = {
        "PATH": str(Path(sys.executable).parent) + os.pathsep + os.defpath,
        "HOME": str(home),
        "LANG": "C.UTF-8",
        **(
            {"SYSTEMROOT": os.environ["SYSTEMROOT"]}
            if "SYSTEMROOT" in os.environ
            else {}
        ),
    }
    commands = {}
    for role in ("client", "server", "both"):
        command = [
            backend,
            "--harn",
            executable,
            "--file",
            str(fixture / "server.harn"),
            "--ir",
            str(fixture / "ir.json"),
            "--role",
            role,
            "--out",
            str(scratch / role),
            "--plugin-read-root",
            sys.prefix,
        ]
        generated = subprocess.run(
            command,
            cwd=scratch,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        (scratch / f"generate-{role}.stderr").write_text(generated.stderr)
        assert generated.returncode == 0, generated.stderr
        checked = subprocess.run(
            [*command, "--check"],
            cwd=scratch,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        assert checked.returncode == 0, checked.stderr
        assert (scratch / role / "bindings.py").stat().st_size > 0
        commands[role] = command
    path = scratch / "both/bindings.py"
    original = path.read_bytes()
    modified = original + b"\n# deliberate drift\n"
    path.write_bytes(modified)
    drift = subprocess.run(
        [*commands["both"], "--check"],
        cwd=scratch,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert drift.returncode == 2 and path.read_bytes() == modified
    assert (
        CodegenDiagnostic.model_validate_json(drift.stderr).code.value
        == "artifact_drift"
    )
    path.write_bytes(original)
    spec = importlib.util.spec_from_file_location("harn_product_bindings", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    payload = (fixture / "input.json").read_text().strip()
    expected = loads(payload)
    arguments = TypeAdapter(module.EchoInput).validate_json('{"input":' + payload + "}")
    server = subprocess.Popen(
        [
            executable,
            "serve",
            "mcp",
            "--surface",
            "exports",
            "--transport",
            "http",
            "--bind",
            "127.0.0.1:0",
            "--obs",
            "off",
            str(fixture / "server.harn"),
        ],
        cwd=scratch,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    ready = queue.Queue()
    logs = []

    def read_server():
        assert server.stderr is not None
        for line in server.stderr:
            logs.append(line)
            match = re.search(
                r"MCP workflow server ready on (http://127\.0\.0\.1:[0-9]+)/mcp", line
            )
            if match:
                ready.put(match.group(1))

    reader = threading.Thread(target=read_server)
    reader.start()
    try:
        base_url = ready.get(timeout=30)
        adapter = TypeAdapter(module.Payload)
        response_media = []

        def observe_response(response):
            assert "authorization" not in response.request.headers
            assert set(response.request.headers["accept"].split(", ")) == {
                "application/json",
                "text/event-stream",
            }
            response_media.append(
                (
                    response.request.headers[facts.MCP_HEADER_METHOD],
                    response.headers["content-type"].split(";", 1)[0],
                )
            )

        with (
            httpx.Client(
                base_url=base_url, event_hooks={"response": [observe_response]}
            ) as http,
            HarnClient(base_url=base_url, client=http) as transport,
        ):
            client = module.Client(transport)
            assert (
                loads(
                    adapter.dump_json(
                        client.echo(arguments), by_alias=True, exclude_unset=True
                    )
                )
                == expected
            )
            failure = client.reject(arguments)
            assert (
                isinstance(failure, ApplicationFailure)
                and failure.error.variant == "Rejected"
            )
            assert (
                loads(
                    adapter.dump_json(
                        client.scheduled(arguments), by_alias=True, exclude_unset=True
                    )
                )
                == expected
            )

        async def asynchronous():
            async def observe(response):
                observe_response(response)

            async with (
                httpx.AsyncClient(
                    base_url=base_url, event_hooks={"response": [observe]}
                ) as http,
                AsyncHarnClient(base_url=base_url, client=http) as transport,
            ):
                client = module.AsyncClient(transport)
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

        asyncio.run(asynchronous())
        assert {media for _, media in response_media} == {
            "application/json",
            "text/event-stream",
        }
        sys.path.insert(0, str(ROOT))
        from examples.fastapi_generated import create_app

        reached = []
        with TestClient(create_app(base_url)) as app:
            for route in ("echo-sync", "echo-async", "scheduled"):
                result = app.post(
                    "/" + route,
                    content='{"input":' + payload + "}",
                    headers={"content-type": "application/json"},
                )
                assert result.status_code == 200, (route, result.status_code)
                assert loads(result.content) == expected
                reached.append(route)
            assert app.post("/echo-sync", json={"input": {}}).status_code == 422
            negative_zero = payload.replace(
                '"sequence":9223372036854775807', '"sequence":-0'
            )
            assert negative_zero != payload
            assert (
                app.post(
                    "/echo-sync",
                    content='{"input":' + negative_zero + "}",
                    headers={"content-type": "application/json"},
                ).status_code
                == 422
            )
        receipt = {
            "runtime_sha256": hashlib.sha256(Path(executable).read_bytes()).hexdigest(),
            "scratch": str(scratch),
            "installed_sdk": harn.__file__,
            "identity": json.loads((fixture / "ir.json").read_bytes())["identity"],
            "shared_payload_sha256": hashlib.sha256(
                (fixture / "input.json").read_bytes()
            ).hexdigest(),
            "generated_roles": list(commands),
            "determinism_checked_by_host": True,
            "drift_refused_and_preserved": True,
            "sync_echo_reject_task": True,
            "async_echo_reject_task": True,
            "http_responses_observed": response_media,
            "fastapi_reached": reached,
            "malformed_input_refused": True,
            "input_refusals": ["missing_payload_fields", "integer_negative_zero"],
            "pending": 0,
        }
    finally:
        if server.poll() is None:
            server.send_signal(signal.SIGINT)
        try:
            try:
                server.wait(timeout=30)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=30)
                raise AssertionError(
                    "Recorded Harn server did not stop after SIGINT"
                ) from None
        finally:
            reader.join(timeout=30)
            assert not reader.is_alive()
            (scratch / "harn.log").write_text("".join(logs))
    from codegen_product_native import qualify_native

    receipt["native"] = qualify_native(
        executable, scratch, ROOT / "tests/fixtures/codegen", path, module, payload
    )
    installed = Path(harn.__file__).parent
    files = sorted(
        path
        for path in installed.rglob("*")
        if path.is_file() and path.suffix in (".py", ".json")
    )
    assert len(files) >= 85
    digest = hashlib.sha256()
    for file in files:
        digest.update(file.relative_to(installed).as_posix().encode() + b"\0")
        digest.update(file.read_bytes())
    receipt["sdk"] = {
        "version": version("harn-sdk"),
        "files_observed": len(files),
        "source_sha256": digest.hexdigest(),
        "mcp": version("mcp"),
        "pydantic": version("pydantic"),
    }
    receipt.update(status="passed", pending=0, failing_names=[])
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
