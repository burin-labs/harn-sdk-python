import json
from decimal import Decimal, localcontext

import pytest
from pydantic import TypeAdapter, ValidationError

from harn.bindings import WireBytes, WireDecimal


def test_bytes_roundtrip_exact_binary_envelope_and_empty_value():
    adapter = TypeAdapter(WireBytes)
    for value in (b"", b"\x00\xff\x80binary"):
        encoded = adapter.dump_json(adapter.validate_python(value, strict=True))
        assert list(json.loads(encoded)) == ["$bytes_b64"]
        assert adapter.validate_json(encoded, strict=True) == value


@pytest.mark.parametrize(
    "value",
    [
        "YQ==",
        {"$bytes_b64": "YQ==", "extra": True},
        {"$bytes_b64": "YQ"},
        {"$bytes_b64": "YR=="},
        {"$bytes_b64": "YQ==\n"},
        {"$bytes_b64": 1},
        {"$bytes_b64": "-_=="},
        None,
    ],
)
def test_bytes_refuses_malformed_noncanonical_or_unboxed_wire(value):
    with pytest.raises(ValidationError):
        TypeAdapter(WireBytes).validate_json(json.dumps(value), strict=True)


def test_bytes_native_values_are_not_implicitly_encoded_strings():
    with pytest.raises(ValidationError):
        TypeAdapter(WireBytes).validate_python("YQ==", strict=True)


def test_decimal_preserves_scale_and_exact_mantissa_without_context_rounding():
    adapter = TypeAdapter(WireDecimal)
    values = [
        "0",
        "1.00",
        "-123.4500",
        "79228162514264337593543950335",
        "0.0000000000000000000000000001",
    ]
    with localcontext() as context:
        context.prec = 3
        for text in values:
            native = adapter.validate_json(json.dumps(text), strict=True)
            assert native.as_tuple() == Decimal(text).as_tuple()
            assert json.loads(adapter.dump_json(native)) == text


@pytest.mark.parametrize(
    "value",
    [
        "1e2",
        "+1",
        "01",
        "1.",
        ".1",
        "-0.0",
        "NaN",
        "Infinity",
        "79228162514264337593543950336",
        "79228162514264337593543950335.0",
        "0.00000000000000000000000000001",
        1,
        1.0,
        None,
    ],
)
def test_decimal_refuses_noncanonical_spelling_or_unrepresentable_value(value):
    with pytest.raises(ValidationError):
        TypeAdapter(WireDecimal).validate_json(json.dumps(value), strict=True)


def test_native_decimal_positive_exponents_are_encoded_without_unbounded_expansion():
    adapter = TypeAdapter(WireDecimal)
    assert (
        adapter.dump_json(adapter.validate_python(Decimal("1E+2"), strict=True))
        == b'"100"'
    )
    assert (
        adapter.dump_json(adapter.validate_python(Decimal("0E+999999999"), strict=True))
        == b'"0"'
    )
    with pytest.raises(ValidationError):
        adapter.validate_python(Decimal("1E+999999999"), strict=True)
    for value in ("1.00", 1, Decimal("NaN"), Decimal("-0.0")):
        with pytest.raises(ValidationError):
            adapter.validate_python(value, strict=True)
