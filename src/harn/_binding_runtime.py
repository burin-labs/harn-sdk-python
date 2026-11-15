"""Typed invocation boundaries used by generated clients and native handlers."""

from __future__ import annotations

import inspect
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Literal, TypeVar, overload

from pydantic import MISSING, JsonValue, TypeAdapter, ValidationError

from ._codegen.protocol import HARN_MCP_TOOL_CONTRACT_META_KEY
from .bindings import ApplicationFailure, BindingError, WireModel

I = TypeVar("I")
O = TypeVar("O")
E = TypeVar("E")
_JSON = TypeAdapter(JsonValue)


def decode_wire(adapter: TypeAdapter[O], value: JsonValue) -> O:
    try:
        return adapter.validate_json(
            json.dumps(value, allow_nan=False),
            strict=True,
            by_alias=True,
            by_name=False,
        )
    except (ValidationError, ValueError, TypeError):
        raise BindingError("invalid_wire_value") from None


def encode_wire(adapter: TypeAdapter[I], value: I) -> JsonValue:
    try:
        validated = adapter.validate_python(
            value, strict=True, by_alias=True, by_name=True
        )
        return _JSON.validate_json(
            adapter.dump_json(
                validated, by_alias=True, exclude_unset=True, warnings="error"
            )
        )
    except (ValidationError, ValueError, TypeError):
        raise BindingError("invalid_native_value") from None


class _ApplicationError(WireModel):
    tool: str
    data: JsonValue
    outcome: Literal["error", "rejected"] | MISSING = MISSING


@overload
def decode_result(
    name: str,
    result: dict[str, JsonValue],
    output: TypeAdapter[O],
    error: None,
    *,
    result_property: bool,
) -> O: ...


@overload
def decode_result(
    name: str,
    result: dict[str, JsonValue],
    output: TypeAdapter[O],
    error: TypeAdapter[E],
    *,
    result_property: bool,
) -> O | ApplicationFailure[E]: ...


def decode_result(
    name: str,
    result: dict[str, JsonValue],
    output: TypeAdapter[O],
    error: TypeAdapter[E] | None,
    *,
    result_property: bool,
) -> O | ApplicationFailure[E]:
    if result.get("resultType") != "complete" or (
        "isError" in result and type(result["isError"]) is not bool
    ):
        raise BindingError("tool_result_unmeasured", name)
    meta = result.get("_meta", {})
    if not isinstance(meta, dict):
        raise BindingError("tool_metadata_unmeasured", name)
    contract = meta.get(HARN_MCP_TOOL_CONTRACT_META_KEY, {})
    if not isinstance(contract, dict):
        raise BindingError("tool_contract_unmeasured", name)
    if result.get("isError", False):
        if "applicationError" not in contract:
            raise BindingError("tool_runtime_failure", name)
        if error is None:
            raise BindingError("undeclared_application_failure", name)
        if "structuredContent" in result:
            raise BindingError("application_failure_ambiguous", name)
        try:
            failure = _ApplicationError.model_validate(contract["applicationError"])
        except ValidationError:
            raise BindingError("application_failure_unmeasured", name) from None
        if failure.tool != name:
            raise BindingError("application_failure_identity", name)
        return ApplicationFailure[E](
            error=decode_wire(error, failure.data),
            outcome=None if failure.outcome is MISSING else failure.outcome,
        )
    if "applicationError" in contract or "structuredContent" not in result:
        raise BindingError("tool_result_unmeasured", name)
    value = result["structuredContent"]
    if result_property:
        if not isinstance(value, dict) or set(value) != {"result"}:
            raise BindingError("tool_output_envelope", name)
        value = value["result"]
    return decode_wire(output, value)


def _handler_result(
    name: str,
    value: O | ApplicationFailure[E],
    output: TypeAdapter[O],
    error: TypeAdapter[E] | None,
    *,
    result_property: bool,
) -> dict[str, JsonValue]:
    if isinstance(value, ApplicationFailure):
        if error is None:
            raise BindingError("undeclared_application_failure", name)
        try:
            validated = ApplicationFailure.model_validate(value)
        except ValidationError:
            raise BindingError("invalid_native_application_failure", name) from None
        data = encode_wire(error, validated.error)
        failure: dict[str, JsonValue] = {"tool": name, "data": data}
        if validated.outcome is not None:
            failure["outcome"] = validated.outcome
        return {
            "resultType": "complete",
            "isError": True,
            "content": [{"type": "text", "text": "Declared application failure"}],
            "_meta": {HARN_MCP_TOOL_CONTRACT_META_KEY: {"applicationError": failure}},
        }
    data = encode_wire(output, value)
    return {
        "resultType": "complete",
        "isError": False,
        "content": [{"type": "text", "text": json.dumps(data, allow_nan=False)}],
        "structuredContent": {"result": data} if result_property else data,
    }


def _async_callable(handler: Callable[[I], O]) -> bool:
    return inspect.iscoroutinefunction(handler) or inspect.iscoroutinefunction(
        handler.__call__
    )


@dataclass(frozen=True)
class SyncBinding:
    operation_id: str
    name: str
    invoke: Callable[[JsonValue], dict[str, JsonValue]]


@dataclass(frozen=True)
class AsyncBinding:
    operation_id: str
    name: str
    invoke: Callable[[JsonValue], Awaitable[dict[str, JsonValue]]]


def bind_sync(
    operation_id: str,
    name: str,
    handler: Callable[[I], O | ApplicationFailure[E]],
    input: TypeAdapter[I],
    output: TypeAdapter[O],
    error: TypeAdapter[E] | None,
    *,
    result_property: bool,
) -> SyncBinding:
    if not callable(handler) or _async_callable(handler):
        raise BindingError("expected_sync_handler", name)

    def invoke(arguments: JsonValue) -> dict[str, JsonValue]:
        payload = decode_wire(input, arguments)
        result = handler(payload)
        if inspect.isawaitable(result):
            if inspect.iscoroutine(result):
                result.close()
            raise BindingError("expected_sync_result", name)
        return _handler_result(
            name, result, output, error, result_property=result_property
        )

    return SyncBinding(operation_id, name, invoke)


def bind_async(
    operation_id: str,
    name: str,
    handler: Callable[[I], Awaitable[O | ApplicationFailure[E]]],
    input: TypeAdapter[I],
    output: TypeAdapter[O],
    error: TypeAdapter[E] | None,
    *,
    result_property: bool,
) -> AsyncBinding:
    if not callable(handler) or not _async_callable(handler):
        raise BindingError("expected_async_handler", name)

    async def invoke(arguments: JsonValue) -> dict[str, JsonValue]:
        return _handler_result(
            name,
            await handler(decode_wire(input, arguments)),
            output,
            error,
            result_property=result_property,
        )

    return AsyncBinding(operation_id, name, invoke)
