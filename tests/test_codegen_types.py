"""Isolated rendering controls; host validation separately admits semantic IR."""

import importlib.util
import sys

from pydantic import TypeAdapter

from harn._codegen.render import render_types
from harn._codegen.request import CodegenIr


def ir_with_types(types):
    source = {"kind": "synthetic", "owner": "renderer-control"}
    return CodegenIr.model_validate(
        {
            "schema_version": "harn-codegen/1.0",
            "required_features": [],
            "identity": dict.fromkeys(
                ["catalog_digest", "binding_digest", "ir_digest"], "a" * 64
            ),
            "catalog_canonical_json": "opaque",
            "sources": [source],
            "package": {"id": "test", "name": "test", "source": source},
            "types": [{"source": source, **wire} for wire in types],
            "operations": [],
            "mcp_tools": [],
        }
    )


def load(tmp_path, artifact):
    path = tmp_path / artifact.path
    path.write_text(artifact.content)
    spec = importlib.util.spec_from_file_location("harn_codegen_renderer_control", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_field_matching_a_type_symbol_keeps_wire_name_without_breaking_annotations(
    tmp_path,
):
    source = {"kind": "synthetic", "owner": "renderer-control"}
    ir = ir_with_types(
        [
            {"id": "text", "name": "Text", "shape": {"kind": "string"}},
            {
                "id": "container",
                "name": "Container",
                "shape": {
                    "kind": "record",
                    "fields": [
                        {
                            "id": "field",
                            "name": "Text",
                            "type_id": "text",
                            "optional": False,
                            "source": source,
                        }
                    ],
                },
            },
        ]
    )
    artifact = render_types(ir)
    module = load(tmp_path, artifact)
    adapter = TypeAdapter(module.Container)
    value = adapter.validate_json('{"Text":"kept"}', strict=True)
    assert adapter.dump_json(value, by_alias=True) == b'{"Text":"kept"}'
    assert "Text" not in module.Container.model_fields
    assert len(artifact.source_mappings) == 2


def test_float_literal_refuses_integer_token_and_keeps_source_mappings(tmp_path):
    ir = ir_with_types(
        [
            {
                "id": "one",
                "name": "One",
                "shape": {
                    "kind": "literal",
                    "value": {"kind": "float", "value": "1.0"},
                },
            }
        ]
    )
    artifact = render_types(ir)
    module = load(tmp_path, artifact)
    adapter = TypeAdapter(module.One)
    assert adapter.validate_json("1.0", strict=True) == 1.0
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        adapter.validate_json("1", strict=True)
    mapped = artifact.source_mappings[0]
    assert b"TypeAliasType" in artifact.content.encode()[mapped.start : mapped.end]


def test_json_tuple_under_bounded_record_keeps_native_tuple_strict(tmp_path):
    import pytest
    from pydantic import ValidationError

    source = {"kind": "synthetic", "owner": "renderer-control"}
    ir = ir_with_types(
        [
            {"id": "text", "name": "Text", "shape": {"kind": "string"}},
            {
                "id": "pair",
                "name": "Pair",
                "shape": {"kind": "tuple", "items": ["text"]},
            },
            {
                "id": "box",
                "name": "Box",
                "shape": {
                    "kind": "record",
                    "fields": [
                        {
                            "id": "item",
                            "name": "item",
                            "type_id": "pair",
                            "optional": False,
                            "source": source,
                        }
                    ],
                },
            },
        ]
    )
    module = load(tmp_path, render_types(ir))
    adapter = TypeAdapter(module.Box)
    assert adapter.validate_json('{"item":["kept"]}', strict=True).item == ("kept",)
    assert module.Box(item=("kept",)).item == ("kept",)
    with pytest.raises(ValidationError):
        module.Box(item=["kept"])


def test_float_widens_integer_values_while_integer_tokens_stay_exact(tmp_path):
    import pytest
    from pydantic import ValidationError

    from harn.bindings import BindingError, parse_wire_json

    module = load(
        tmp_path,
        render_types(
            ir_with_types(
                [
                    {"id": "number", "name": "Number", "shape": {"kind": "float"}},
                    {
                        "id": "integer",
                        "name": "Integer",
                        "shape": {
                            "kind": "integer",
                            "encoding": "json_number",
                            "minimum": "-9223372036854775808",
                            "maximum": "9223372036854775807",
                        },
                    },
                ]
            )
        ),
    )
    floating = TypeAdapter(module.Number)
    assert floating.validate_json("1", strict=True) == 1.0
    assert type(floating.validate_json("1", strict=True)) is float
    assert floating.validate_python(1, strict=True) == 1.0
    for invalid in ("true", '"1"', "NaN", "Infinity"):
        with pytest.raises(ValidationError):
            floating.validate_json(invalid, strict=True)
    for invalid in ("1.0", "-0", "true"):
        with pytest.raises(BindingError):
            parse_wire_json(TypeAdapter(module.Integer), invalid)
    # Pydantic has already erased this lexical distinction before field validators run.
    assert TypeAdapter(module.Integer).validate_json("-0", strict=True) == 0
    assert parse_wire_json(TypeAdapter(module.Number), "-0") == -0.0
