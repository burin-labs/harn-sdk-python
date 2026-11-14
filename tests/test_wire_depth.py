import json
from typing import Annotated

import pytest
from pydantic import TypeAdapter, ValidationError, WrapValidator
from typing_extensions import TypeAliasType

from harn._codegen.protocol import WIRE_MAX_VALUE_DEPTH
from harn._wire_depth import wire_value_depth

Recursive = TypeAliasType(
    "Recursive", Annotated[list["Recursive"], WrapValidator(wire_value_depth)]
)
Transparent = TypeAliasType("Transparent", Recursive)


def nested(depth):
    value = []
    for _ in range(depth):
        value = [value]
    return value


def test_exact_wire_depth_boundary_and_transparent_aliases():
    for target in (Recursive, Transparent):
        adapter = TypeAdapter(target)
        encoded = json.dumps(nested(WIRE_MAX_VALUE_DEPTH))
        assert adapter.validate_json(encoded, strict=True) == nested(
            WIRE_MAX_VALUE_DEPTH
        )
        with pytest.raises(ValidationError):
            adapter.validate_json(
                json.dumps(nested(WIRE_MAX_VALUE_DEPTH + 1)), strict=True
            )
        # A failed branch must not leak its ContextVar count into another call.
        assert adapter.validate_json("[]", strict=True) == []
