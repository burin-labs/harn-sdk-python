"""Native Python values for Harn's generated scalar wire encodings."""

from __future__ import annotations

import base64
import binascii
import re
from decimal import Decimal
from typing import Annotated, cast

from pydantic import BeforeValidator, PlainSerializer, ValidationInfo

from ._codegen.protocol import (
    WIRE_BYTES_TAG,
    WIRE_DECIMAL_MAX_MANTISSA,
    WIRE_DECIMAL_MAX_SCALE,
    WIRE_DECIMAL_PATTERN,
    WIRE_DECIMAL_PRESERVES_NEGATIVE_ZERO,
    WIRE_DECIMAL_PRESERVES_SCALE,
)

_DECIMAL_PATTERN = re.compile(WIRE_DECIMAL_PATTERN)
_MAX_MANTISSA = int(WIRE_DECIMAL_MAX_MANTISSA)


def _bytes(value: object, info: ValidationInfo) -> bytes:
    if info.mode == "python":
        if type(value) is not bytes:
            raise ValueError("invalid native bytes")
        return value
    if type(value) is not dict or set(value) != {WIRE_BYTES_TAG}:
        raise ValueError("invalid wire bytes envelope")
    encoded = value[WIRE_BYTES_TAG]
    if type(encoded) is not str:
        raise ValueError("invalid wire base64")
    try:
        decoded = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as error:
        raise ValueError("invalid wire base64") from error
    if base64.b64encode(decoded).decode("ascii") != encoded:
        raise ValueError("noncanonical wire base64")
    return decoded


def _encode_bytes(value: bytes) -> dict[str, str]:
    return {WIRE_BYTES_TAG: base64.b64encode(value).decode("ascii")}


def _decimal_text(value: Decimal) -> str:
    if not WIRE_DECIMAL_PRESERVES_SCALE or not value.is_finite():
        raise ValueError("unsupported or invalid wire decimal")
    if (
        not WIRE_DECIMAL_PRESERVES_NEGATIVE_ZERO
        and value.is_signed()
        and value.is_zero()
    ):
        raise ValueError("noncanonical wire decimal")
    parts = value.as_tuple()
    exponent = cast("int", parts.exponent)  # Finite Decimal exponents are integers.
    if -exponent > WIRE_DECIMAL_MAX_SCALE:
        raise ValueError("wire decimal scale exceeded")
    # Decimal arithmetic obeys the caller's active precision. Inspect its exact
    # coefficient instead, including any zeros needed by a positive exponent.
    if len(parts.digits) > len(WIRE_DECIMAL_MAX_MANTISSA):
        raise ValueError("wire decimal magnitude exceeded")
    coefficient = int("".join(str(digit) for digit in parts.digits))
    if exponent > 0:
        # Bound before exponentiation to refuse extreme native exponents cheaply.
        if coefficient and len(parts.digits) + exponent > len(
            WIRE_DECIMAL_MAX_MANTISSA
        ):
            raise ValueError("wire decimal magnitude exceeded")
        coefficient *= 10 ** min(exponent, len(WIRE_DECIMAL_MAX_MANTISSA))
    if coefficient > _MAX_MANTISSA:
        raise ValueError("wire decimal magnitude exceeded")
    text = str(coefficient) if exponent > 0 else format(value, "f")
    if exponent > 0 and parts.sign:
        text = "-" + text
    if _DECIMAL_PATTERN.fullmatch(text) is None:
        raise ValueError("invalid wire decimal")
    return text


def _decimal(value: object, info: ValidationInfo) -> Decimal:
    if info.mode == "python":
        if type(value) is not Decimal:
            raise ValueError("invalid native decimal")
        _decimal_text(value)
        return value
    if type(value) is not str or _DECIMAL_PATTERN.fullmatch(value) is None:
        raise ValueError("invalid wire decimal")
    decoded = Decimal(value)
    if _decimal_text(decoded) != value:
        raise ValueError("noncanonical wire decimal")
    return decoded


WireBytes = Annotated[
    bytes,
    BeforeValidator(_bytes),
    PlainSerializer(_encode_bytes, return_type=dict[str, str], when_used="json"),
]
WireDecimal = Annotated[
    Decimal,
    BeforeValidator(_decimal),
    PlainSerializer(_decimal_text, return_type=str, when_used="json"),
]
