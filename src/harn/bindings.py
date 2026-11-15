"""Shared runtime types for adapters generated from Harn's closed codegen IR."""

from __future__ import annotations

from collections.abc import Callable
from typing import ClassVar, Generic, Literal, Self, TypeVar

from pydantic import (
    MISSING,
    BaseModel,
    ConfigDict,
    JsonValue,
    ModelWrapValidatorHandler,
    TypeAdapter,
    ValidationInfo,
    model_validator,
)

from ._wire_depth import at_value_depth
from ._wire_sets import WireSet
from ._wire_values import WireBytes, WireDecimal

__all__ = [
    "MISSING",
    "ApplicationFailure",
    "BindingError",
    "WireBytes",
    "WireDecimal",
    "WireModel",
    "WireSet",
    "WireValueModel",
    "parse_wire_json",
]

E = TypeVar("E")
T = TypeVar("T")


def parse_wire_json(adapter: TypeAdapter[T], content: bytes | str) -> T:
    """Read exact JSON token kinds, then validate the generated Pydantic shape."""
    from ._binding_runtime import decode_wire
    from ._wire_json import loads

    return decode_wire(adapter, loads(content))


def wire_tuple_validator(value: object, info: ValidationInfo) -> object:
    # Model wrap validators expose JSON arrays as Python lists to nested strict
    # tuple validators. Convert only at the JSON boundary; native lists remain invalid.
    return tuple(value) if info.mode == "json" and type(value) is list else value


def wire_literal_validator(expected: JsonValue) -> Callable[[JsonValue], JsonValue]:
    def validate(value: JsonValue) -> JsonValue:
        if type(value) is not type(expected) or value != expected:
            raise ValueError("invalid wire literal")
        return value

    return validate


class WireModel(BaseModel):
    """Strict typed data: omitted optional fields remain distinct from explicit null."""

    __harn_wire_kind__: ClassVar[Literal["record", "enum"]] = "record"
    __harn_nominal_name__: ClassVar[str | None] = None

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_assignment=True,
        validate_by_alias=True,
        validate_by_name=True,
        revalidate_instances="always",
        allow_inf_nan=False,
        hide_input_in_errors=True,
    )


class ApplicationFailure(WireModel, Generic[E]):
    """Declared application data, kept separate from transport and runtime faults."""

    error: E
    outcome: Literal["error", "rejected"] | None = None


class WireValueModel(WireModel):
    """Generated wire records; native control wrappers don't add wire depth."""

    @model_validator(mode="wrap")
    @classmethod
    def _bounded(cls, value: object, handler: ModelWrapValidatorHandler[Self]) -> Self:
        return at_value_depth(lambda: handler(value))


class BindingError(Exception):
    """An MCP or generated binding failure that is not declared application data."""

    def __init__(self, code: str, operation: str | None = None) -> None:
        self.code = code
        self.operation = operation
        super().__init__(code + (f" (operation {operation})" if operation else ""))
