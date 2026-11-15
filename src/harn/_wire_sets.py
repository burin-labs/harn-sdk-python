"""Ordered set arrays with Harn structural membership, independent of hashing."""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator, Sequence
from decimal import Decimal
from typing import TypeVar, get_args, overload

from pydantic import MISSING, BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema

from ._codegen.protocol import WIRE_MAX_VALUE_DEPTH

T = TypeVar("T")


def _fields(model: BaseModel) -> dict[str, object]:
    fields = {}
    for name, field in type(model).model_fields.items():
        value = getattr(model, name)
        if value is not MISSING:
            fields[field.serialization_alias or name] = value
    fields.update(model.__pydantic_extra__ or {})
    return fields


def _set_equal(left: Sequence[object], right: Sequence[object], depth: int) -> bool:
    if len(left) != len(right):
        return False
    # Mixed Harn int/float equality is lossy and not transitive. Find a full
    # matching instead of sorting, hashing, or greedily reusing a right member.
    left_matches = [-1] * len(left)
    right_matches = [-1] * len(right)
    for root in range(len(left)):
        pending = [root]
        visited = {root}
        parents: dict[int, int] = {}
        endpoint = -1
        while pending and endpoint < 0:
            index = pending.pop(0)
            for candidate, value in enumerate(right):
                if candidate in parents or not _equal(left[index], value, depth):
                    continue
                parents[candidate] = index
                matched = right_matches[candidate]
                if matched < 0:
                    endpoint = candidate
                    break
                if matched not in visited:
                    visited.add(matched)
                    pending.append(matched)
        if endpoint < 0:
            return False
        while endpoint >= 0:
            index = parents[endpoint]
            previous = left_matches[index]
            left_matches[index] = endpoint
            right_matches[endpoint] = index
            endpoint = previous
    return True


def _equal(left: object, right: object, depth: int = 0) -> bool:
    if depth > WIRE_MAX_VALUE_DEPTH:
        raise ValueError("wire value depth exceeded")
    if isinstance(left, WireSet) or isinstance(right, WireSet):
        return (
            isinstance(left, WireSet)
            and isinstance(right, WireSet)
            and _set_equal(left, right, depth + 1)
        )
    if isinstance(left, BaseModel) or isinstance(right, BaseModel):
        left_kind = getattr(type(left), "__harn_wire_kind__", None)
        right_kind = getattr(type(right), "__harn_wire_kind__", None)
        if left_kind == "enum" or right_kind == "enum":
            if (
                left_kind != "enum"
                or right_kind != "enum"
                or not isinstance(left, BaseModel)
                or not isinstance(right, BaseModel)
            ):
                return False
            left_enum, right_enum = _fields(left), _fields(right)
            if set(left_enum) != {"enum", "variant", "fields"} or set(right_enum) != {
                "enum",
                "variant",
                "fields",
            }:
                raise ValueError("invalid native enum set member")
            left_values, right_values = left_enum["fields"], right_enum["fields"]
            if not isinstance(left_values, tuple) or not isinstance(
                right_values, tuple
            ):
                raise ValueError("invalid native enum fields")
            return (
                left_enum["enum"] == right_enum["enum"]
                and left_enum["variant"] == right_enum["variant"]
                and len(left_values) == len(right_values)
                and all(
                    _equal(a, b, depth + 1)
                    for a, b in zip(left_values, right_values, strict=True)
                )
            )
        left_nominal = getattr(type(left), "__harn_nominal_name__", None)
        right_nominal = getattr(type(right), "__harn_nominal_name__", None)
        if left_nominal != right_nominal:
            return False
        if isinstance(left, BaseModel):
            if left_kind != "record":
                raise ValueError("unsupported native set member")
            left = _fields(left)
        if isinstance(right, BaseModel):
            if right_kind != "record":
                raise ValueError("unsupported native set member")
            right = _fields(right)
    if isinstance(left, Decimal) or isinstance(right, Decimal):
        return (
            isinstance(left, Decimal) and isinstance(right, Decimal) and left == right
        )
    if type(left) is bool or type(right) is bool:
        return type(left) is bool and type(right) is bool and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if (type(left) is float and not math.isfinite(left)) or (
            type(right) is float and not math.isfinite(right)
        ):
            raise ValueError("invalid native set member")
        if type(left) is type(right):
            return left == right
        return float(left) == float(right)
    if isinstance(left, (list, tuple)) or isinstance(right, (list, tuple)):
        return (
            isinstance(left, (list, tuple))
            and isinstance(right, (list, tuple))
            and len(left) == len(right)
            and all(_equal(a, b, depth + 1) for a, b in zip(left, right, strict=True))
        )
    if isinstance(left, dict) or isinstance(right, dict):
        return (
            isinstance(left, dict)
            and isinstance(right, dict)
            and left.keys() == right.keys()
            and all(_equal(value, right[key], depth + 1) for key, value in left.items())
        )
    if left is None or right is None:
        return left is None and right is None
    if type(left) in (str, bytes) and type(right) in (str, bytes):
        return type(left) is type(right) and left == right
    if type(left) in (str, bytes) or type(right) in (str, bytes):
        return False
    raise ValueError("unsupported native set member")


def _unique(values: Iterable[T]) -> tuple[T, ...]:
    seen: list[T] = []
    for value in values:
        if not _equal(value, value):
            raise ValueError("invalid native set member")
        if any(_equal(value, previous) for previous in seen):
            raise ValueError("duplicate wire set member")
        seen.append(value)
    return tuple(seen)


class WireSet(Sequence[T]):
    """Immutable ordered members with Harn structural equality and membership."""

    __slots__ = ("_values",)
    _values: tuple[T, ...]

    def __init__(self, values: Iterable[T] = ()) -> None:
        object.__setattr__(self, "_values", _unique(values))

    def __setattr__(self, _name: str, _value: object) -> None:
        raise AttributeError("WireSet is immutable")

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[T]:
        return iter(self._values)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> tuple[T, ...]: ...

    def __getitem__(self, index: int | slice) -> T | tuple[T, ...]:
        return self._values[index]

    def __contains__(self, value: object) -> bool:
        return any(_equal(value, member) for member in self._values)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, WireSet) and _set_equal(self, other, 0)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: object, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        arguments = get_args(source_type)
        if len(arguments) != 1:
            raise TypeError("WireSet requires an item type")
        items = core_schema.list_schema(handler.generate_schema(arguments[0]))
        native = core_schema.chain_schema(
            [
                core_schema.is_instance_schema(cls),
                core_schema.no_info_before_validator_function(list, items),
            ]
        )
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.json_or_python_schema(json_schema=items, python_schema=native),
            serialization=core_schema.plain_serializer_function_ser_schema(
                list, return_schema=items, when_used="json"
            ),
        )
