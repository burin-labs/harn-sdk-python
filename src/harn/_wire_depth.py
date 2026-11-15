"""Count semantic wire nodes, excluding transparent type aliases and envelopes."""

from collections.abc import Callable
from contextvars import ContextVar
from typing import TypeVar

from pydantic import ValidatorFunctionWrapHandler

from ._codegen.protocol import WIRE_MAX_VALUE_DEPTH

T = TypeVar("T")
_DEPTH = ContextVar("harn_wire_value_depth", default=-1)


def at_value_depth(action: Callable[[], T]) -> T:
    depth = _DEPTH.get() + 1
    if depth > WIRE_MAX_VALUE_DEPTH:
        raise ValueError("wire value depth exceeded")
    token = _DEPTH.set(depth)
    try:
        return action()
    finally:
        _DEPTH.reset(token)


def wire_value_depth(value: object, handler: ValidatorFunctionWrapHandler) -> object:
    return at_value_depth(lambda: handler(value))
