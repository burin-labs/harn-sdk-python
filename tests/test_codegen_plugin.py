"""One-shot protocol responses and closed diagnostics stay value-free."""

import json
import subprocess
import sys
from pathlib import Path

from harn._codegen.diagnostic import CodegenDiagnostic
from harn._codegen.response import CodegenResponse

FIXTURE = Path(__file__).parent / "fixtures/codegen/pathological/ir.json"


def invoke(request):
    return subprocess.run(
        [sys.executable, "-m", "harn.codegen"],
        input=json.dumps(request),
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def request():
    return {
        "schema_version": "harn-codegen-request/1.0",
        "role": "both",
        "ir": json.loads(FIXTURE.read_bytes()),
    }


def test_plugin_is_deterministic_and_binds_all_three_digests():
    first, second = invoke(request()), invoke(request())
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout and first.stderr == second.stderr == ""
    response = CodegenResponse.model_validate_json(first.stdout)
    assert response.identity.model_dump() == request()["ir"]["identity"]
    assert response.artifacts and response.artifacts[0].source_mappings
    assert len(response.supported_features) == 13


def test_unknown_contract_never_emits_artifacts_or_rejected_values():
    for change in ("version", "feature", "shape"):
        malformed = request()
        if change == "version":
            malformed["schema_version"] = "secret-value-future-version"
        elif change == "feature":
            malformed["ir"]["required_features"] = ["secret-value-unknown-feature"]
        else:
            malformed["ir"]["types"][0]["shape"]["kind"] = "secret-value-unknown-shape"
        result = invoke(malformed)
        assert result.returncode == 2 and result.stdout == ""
        diagnostic = CodegenDiagnostic.model_validate_json(result.stderr)
        assert (
            diagnostic.code.value
            == {
                "version": "unsupported_version",
                "feature": "unsupported_feature",
                "shape": "invalid_ir",
            }[change]
        )
        assert "secret-value" not in result.stderr


def test_target_refusal_reports_operation_type_and_source():
    unsupported = request()
    wire = next(
        wire
        for wire in unsupported["ir"]["types"]
        if wire["shape"]["kind"] == "enum"
        and wire["shape"]["nominal"]["name"] == "Failure"
    )
    wire["shape"]["variants"] = []
    result = invoke(unsupported)
    assert result.returncode == 2 and result.stdout == ""
    diagnostic = CodegenDiagnostic.model_validate_json(result.stderr)
    assert diagnostic.code.value == "unsupported_wire_type"
    assert (
        diagnostic.type_id == wire["id"]
        and diagnostic.source.model_dump() == wire["source"]
    )
    assert diagnostic.operation == "operation:reject"


def test_missing_output_refuses_before_emitting_a_guessed_handler_contract():
    missing = request()
    operation = missing["ir"]["operations"][0]
    operation["output"] = {"kind": "missing"}
    result = invoke(missing)
    assert result.returncode == 2 and result.stdout == ""
    diagnostic = CodegenDiagnostic.model_validate_json(result.stderr)
    assert diagnostic.code.value == "missing_output"
    assert diagnostic.operation == operation["id"]
    assert diagnostic.source.model_dump() == operation["source"]


def test_a_known_but_unimplemented_feature_refuses_instead_of_claiming_support(
    monkeypatch, capsys
):
    import io

    from harn import codegen

    monkeypatch.setattr(codegen, "SUPPORTED_FEATURES", ())
    monkeypatch.setattr(
        sys, "stdin", io.TextIOWrapper(io.BytesIO(json.dumps(request()).encode()))
    )
    assert codegen.plugin() == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert (
        CodegenDiagnostic.model_validate_json(captured.err).code.value
        == "unsupported_feature"
    )
