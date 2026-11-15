"""The SDK projects the closed IR schema; Harn separately validates IR semantics/digests."""

import copy
import json
from collections.abc import Mapping
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from harn._codegen import protocol
from harn._codegen.request import CodegenRequest

SCHEMA = Path(__file__).parents[1] / "src/harn/_codegen/schemas/request-v1.json"


def test_protocol_constants_match_every_owning_json_fact() -> None:
    def json_projection(value):
        if isinstance(value, Mapping):
            return {key: json_projection(item) for key, item in value.items()}
        if isinstance(value, tuple):
            return [json_projection(item) for item in value]
        return value

    facts = json.loads(SCHEMA.with_name("protocol-v1.json").read_text())
    assert facts
    assert {name: json_projection(getattr(protocol, name)) for name in facts} == facts


def structural_request():
    source = {"kind": "synthetic", "owner": "schema-projection-control"}
    return {
        "schema_version": "harn-codegen-request/1.0",
        "role": "both",
        "ir": {
            "schema_version": "harn-codegen/1.0",
            "required_features": ["exact_json_integer"],
            "identity": {
                key: "a" * 64
                for key in ("catalog_digest", "binding_digest", "ir_digest")
            },
            "catalog_canonical_json": "opaque to this SDK",
            "sources": [],
            "package": {"id": "package", "name": "projection", "source": source},
            "types": [{"id": "string", "source": source, "shape": {"kind": "string"}}],
            "operations": [
                {
                    "id": "echo",
                    "name": "echo",
                    "source": source,
                    "input": "string",
                    "output": {
                        "kind": "value",
                        "type_id": "string",
                        "mcp_envelope": "result_property",
                    },
                    "execution": {
                        "task_support": "optional",
                        "cancellation": "mcp_request",
                    },
                    "governance": {"audiences": ["mcp"]},
                    "cli": {"command": ["echo"], "hidden": False},
                    "binding": {
                        "kind": "harn_export",
                        "operation": "echo",
                        "source": source,
                    },
                }
            ],
            "mcp_tools": [{"opaque": {"oneOf": [{"$ref": "never interpreted"}]}}],
        },
    }


def test_real_schema_projection_preserves_opaque_data_and_nonnull_operations() -> None:
    request = structural_request()
    validator = Draft202012Validator(json.loads(SCHEMA.read_text()))
    validator.validate(request)
    parsed = CodegenRequest.model_validate_json(json.dumps(request))
    assert len(parsed.ir.operations) == 1
    assert parsed.ir.mcp_tools == request["ir"]["mcp_tools"]
    assert parsed.ir.catalog_canonical_json == "opaque to this SDK"


@pytest.mark.parametrize(
    "case",
    ["version", "feature", "unknown", "opaque-array", "wire-kind", "default-null"],
)
def test_projection_and_owning_schema_refuse_the_same_invalid_shapes(case: str) -> None:
    request = copy.deepcopy(structural_request())
    if case == "version":
        request["schema_version"] = "harn-codegen-request/99.0"
    elif case == "feature":
        request["ir"]["required_features"] = ["unknown_future_feature"]
    elif case == "unknown":
        request["ir"]["types"][0]["unexpected"] = "not permitted"
    elif case == "opaque-array":
        request["ir"]["mcp_tools"] = {}
    elif case == "wire-kind":
        request["ir"]["types"][0]["shape"]["kind"] = "any"
    else:
        request["ir"]["operations"][0]["cli"]["aliases"] = None
    validator = Draft202012Validator(json.loads(SCHEMA.read_text()))
    assert list(validator.iter_errors(request)), case
    with pytest.raises(ValidationError):
        CodegenRequest.model_validate_json(json.dumps(request))
