"""Read MCP JSON without erasing the distinction between integer and -0 tokens."""

from __future__ import annotations

import json
import math
import re

from pydantic import JsonValue, TypeAdapter, ValidationError

from ._codegen.protocol import WIRE_INTEGER_TOKEN_PATTERN
from .bindings import BindingError

_INTEGER = re.compile(WIRE_INTEGER_TOKEN_PATTERN)
_JSON = TypeAdapter(JsonValue)


def _integer(token: str) -> int | float:
    if _INTEGER.fullmatch(token) is not None:
        return int(token)
    # serde_json represents this otherwise-valid JSON token as floating zero.
    # Keeping its kind lets the integer adapter refuse it while floats accept it.
    if token == "-0":
        return -0.0
    raise ValueError("invalid wire integer token")


def _float(token: str) -> float:
    value = float(token)
    if not math.isfinite(value):
        raise ValueError("nonfinite wire number")
    return value


def _constant(_token: str) -> None:
    raise ValueError("nonstandard JSON number")


def loads(content: bytes | str) -> JsonValue:
    try:
        value = json.loads(
            content, parse_int=_integer, parse_float=_float, parse_constant=_constant
        )
        return _JSON.validate_python(value, strict=True)
    except (ValueError, TypeError, ValidationError, RecursionError):
        raise BindingError("mcp_invalid_json") from None
