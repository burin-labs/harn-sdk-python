"""Consume Harn's compiled naming corpus instead of inventing backend catalogs."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from harn._codegen.api import render
from harn._codegen.request import CodegenIr, CodegenRole
from harn.bindings import BindingError

FIXTURE = Path(__file__).parent / "fixtures/codegen/names.ir.json"


def test_actual_eighteen_name_corpus_compiles_and_roundtrips_all_wire_keys(tmp_path):
    ir = CodegenIr.model_validate_json(FIXTURE.read_bytes())
    assert len(ir.operations) == 18 and len(ir.types) == 25
    artifact = render(ir, CodegenRole.BOTH)
    reordered = ir.model_copy(
        update={
            "types": list(reversed(ir.types)),
            "operations": list(reversed(ir.operations)),
        }
    )
    assert render(reordered, CodegenRole.BOTH) == artifact
    path = tmp_path / artifact.path
    path.write_text(artifact.content)
    spec = importlib.util.spec_from_file_location("shared_name_bindings", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert len(module.SyncHandlers.__required_keys__) == 18
    assert (
        module.SyncHandlers.__required_keys__ == module.AsyncHandlers.__required_keys__
    )
    assert all(
        callable(getattr(module.Client, name))
        and callable(getattr(module.AsyncClient, name))
        for name in module.SyncHandlers.__required_keys__
    )
    called = []

    def echo(value):
        called.append(type(value).__name__)
        assert callable(value.model_dump)
        return value

    server = module.create_server(
        dict.fromkeys(module.SyncHandlers.__required_keys__, echo)
    )
    for operation in ir.operations:
        wire = next(wire for wire in ir.types if wire.id == operation.input)
        payload = {field.name: index for index, field in enumerate(wire.shape.fields)}
        payload.update(
            wire_bytes={"$bytes_b64": "AAE="},
            wire_decimal="1.2300",
            wire_list=[1],
            wire_set=[1, 2],
            wire_map={"key": 1},
            wire_tuple=[{"$bytes_b64": "AAE="}, 1],
        )
        assert len(payload) == 24
        assert (
            server._bindings[operation.name].invoke(payload)["structuredContent"]
            == payload
        )
        with pytest.raises(BindingError, match="invalid_wire_value"):
            server._bindings[operation.name].invoke({**payload, "unknown-extra": 0})
    assert len(called) == len(set(called)) == 18
    config = tmp_path / "pyrightconfig.json"
    config.write_text(
        json.dumps(
            {
                "typeCheckingMode": "strict",
                "include": [artifact.path],
                "pythonVersion": "3.11",
                "extraPaths": [str(Path(__file__).parents[1] / "src")],
            }
        )
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyright",
            "--pythonpath",
            sys.executable,
            "--project",
            str(config),
            "--outputjson",
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    report = json.loads(result.stdout)
    assert result.returncode == 0 and report["generalDiagnostics"] == [], report
