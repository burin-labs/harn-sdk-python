import asyncio

import pytest
from pydantic import MISSING, Field, TypeAdapter

from harn._binding_runtime import (
    bind_async,
    bind_sync,
    decode_result,
    decode_wire,
    encode_wire,
)
from harn._codegen.protocol import HARN_MCP_TOOL_CONTRACT_META_KEY
from harn.bindings import ApplicationFailure, BindingError, WireModel


class Arguments(WireModel):
    value: int


class Output(WireModel):
    result: int


class Failure(WireModel):
    code: str


def test_scalar_wrapper_and_record_named_result_have_distinct_typed_meanings() -> None:
    scalar = bind_sync(
        "scalar",
        "scalar",
        lambda args: args.value + 1,
        TypeAdapter(Arguments),
        TypeAdapter(int),
        None,
        result_property=True,
    )
    record = bind_sync(
        "record",
        "record",
        lambda args: Output(result=args.value + 1),
        TypeAdapter(Arguments),
        TypeAdapter(Output),
        None,
        result_property=False,
    )
    scalar_reply, record_reply = (
        scalar.invoke({"value": 41}),
        record.invoke({"value": 41}),
    )
    assert (
        scalar_reply["structuredContent"]
        == record_reply["structuredContent"]
        == {"result": 42}
    )
    assert (
        decode_result(
            "scalar", scalar_reply, TypeAdapter(int), None, result_property=True
        )
        == 42
    )
    assert decode_result(
        "record", record_reply, TypeAdapter(Output), None, result_property=False
    ) == Output(result=42)


@pytest.mark.parametrize("value", [42, None])
def test_explicit_bare_projection_preserves_any_json_value_and_null_presence(
    value,
) -> None:
    adapter = TypeAdapter(int if value is not None else type(None))
    result = {"resultType": "complete", "isError": False, "structuredContent": value}
    assert decode_result("value", result, adapter, None, result_property=False) == value
    del result["structuredContent"]
    with pytest.raises(BindingError, match="tool_result_unmeasured"):
        decode_result("value", result, adapter, None, result_property=False)


def test_malformed_arguments_fail_before_the_handler_is_reached() -> None:
    called = []

    def handler(args: Arguments) -> Output:
        called.append(args.value)
        return Output(result=args.value)

    bound = bind_sync(
        "operation",
        "echo",
        handler,
        TypeAdapter(Arguments),
        TypeAdapter(Output),
        None,
        result_property=False,
    )
    for payload in ({"value": True}, {"value": "1"}, {"value": 1, "extra": True}, {}):
        with pytest.raises(BindingError, match="invalid_wire_value"):
            bound.invoke(payload)
    assert called == []
    assert bound.invoke({"value": 1})["isError"] is False
    assert called == [1]


def test_subclass_extra_output_and_constructed_wrong_values_fail_before_success() -> (
    None
):
    class Extra(Output):
        extra: bool

    for value in (Extra(result=1, extra=True), Output.model_construct(result="wrong")):
        assert value.model_fields_set
        with pytest.raises(BindingError, match="invalid_native_value"):
            encode_wire(TypeAdapter(Output), value)


def test_only_explicit_declared_failures_become_typed_error_data() -> None:
    def handler(_args: Arguments) -> Output | ApplicationFailure[Failure]:
        return ApplicationFailure[Failure](
            error=Failure(code="missing"), outcome="rejected"
        )

    bound = bind_sync(
        "operation",
        "lookup",
        handler,
        TypeAdapter(Arguments),
        TypeAdapter(Output),
        TypeAdapter(Failure),
        result_property=False,
    )
    reply = bound.invoke({"value": 1})
    assert reply["isError"] is True
    decoded = decode_result(
        "lookup",
        reply,
        TypeAdapter(Output),
        TypeAdapter(Failure),
        result_property=False,
    )
    assert isinstance(decoded, ApplicationFailure)
    assert decoded.error == Failure(code="missing")
    assert decoded.outcome == "rejected"
    with pytest.raises(BindingError, match="tool_runtime_failure"):
        decode_result(
            "lookup",
            {"resultType": "complete", "isError": True},
            TypeAdapter(Output),
            TypeAdapter(Failure),
            result_property=False,
        )
    with pytest.raises(BindingError, match="undeclared_application_failure"):
        decode_result("lookup", reply, TypeAdapter(Output), None, result_property=False)


def test_null_application_data_is_present_while_absent_data_is_unmeasured() -> None:
    reply = {
        "resultType": "complete",
        "isError": True,
        "_meta": {
            HARN_MCP_TOOL_CONTRACT_META_KEY: {
                "applicationError": {"tool": "lookup", "data": None}
            }
        },
    }
    value = decode_result(
        "lookup",
        reply,
        TypeAdapter(Output),
        TypeAdapter(type(None)),
        result_property=False,
    )
    assert isinstance(value, ApplicationFailure) and value.error is None
    del reply["_meta"][HARN_MCP_TOOL_CONTRACT_META_KEY]["applicationError"]["data"]
    with pytest.raises(BindingError, match="application_failure_unmeasured"):
        decode_result(
            "lookup",
            reply,
            TypeAdapter(Output),
            TypeAdapter(type(None)),
            result_property=False,
        )


def test_declared_application_failure_cannot_also_carry_success_data() -> None:
    reply = {
        "resultType": "complete",
        "isError": True,
        "_meta": {
            HARN_MCP_TOOL_CONTRACT_META_KEY: {
                "applicationError": {"tool": "lookup", "data": {"code": "known"}}
            }
        },
    }
    positive = decode_result(
        "lookup",
        reply,
        TypeAdapter(Output),
        TypeAdapter(Failure),
        result_property=False,
    )
    assert isinstance(positive, ApplicationFailure) and positive.error.code == "known"
    for success in ({"result": 999}, {}, None):
        with pytest.raises(BindingError, match="application_failure_ambiguous"):
            decode_result(
                "lookup",
                {**reply, "structuredContent": success},
                TypeAdapter(Output),
                TypeAdapter(Failure),
                result_property=False,
            )


def test_optional_error_flag_defaults_false_without_accepting_malformed_present_values():
    measured = {"resultType": "complete", "structuredContent": {"result": 42}}
    assert (
        decode_result(
            "known", measured, TypeAdapter(Output), None, result_property=False
        ).result
        == 42
    )
    for error_flag in (None, "false", 0, [], {}):
        with pytest.raises(BindingError, match="tool_result_unmeasured"):
            decode_result(
                "known",
                {**measured, "isError": error_flag},
                TypeAdapter(Output),
                None,
                result_property=False,
            )
    for kind in (None, "future", "input_required", "task"):
        malformed = {**measured, "resultType": kind}
        with pytest.raises(BindingError, match="tool_result_unmeasured"):
            decode_result(
                "known", malformed, TypeAdapter(Output), None, result_property=False
            )
    with pytest.raises(BindingError, match="tool_result_unmeasured"):
        decode_result(
            "known",
            {"structuredContent": {"result": 42}},
            TypeAdapter(Output),
            None,
            result_property=False,
        )


def test_python_field_names_do_not_relax_the_canonical_wire_keys() -> None:
    class Aliased(WireModel):
        python_name: str = Field(
            validation_alias="wire-name", serialization_alias="wire-name"
        )
        optional: str | MISSING = MISSING

    value = Aliased(python_name="ok")
    assert encode_wire(TypeAdapter(Aliased), value) == {"wire-name": "ok"}
    assert decode_wire(TypeAdapter(Aliased), {"wire-name": "ok"}) == value
    with pytest.raises(BindingError, match="invalid_wire_value"):
        decode_wire(TypeAdapter(Aliased), {"python_name": "ok"})


@pytest.mark.asyncio
async def test_async_handlers_receive_native_cancellation_after_reached_event() -> None:
    reached, blocked, cancelled = asyncio.Event(), asyncio.Event(), asyncio.Event()

    async def handler(_args: Arguments) -> Output:
        reached.set()
        try:
            await blocked.wait()
        finally:
            cancelled.set()
        return Output(result=1)

    bound = bind_async(
        "operation",
        "wait",
        handler,
        TypeAdapter(Arguments),
        TypeAdapter(Output),
        None,
        result_property=False,
    )
    task = asyncio.create_task(bound.invoke({"value": 1}))
    async with asyncio.timeout(30):
        await reached.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    assert cancelled.is_set()
    with pytest.raises(BindingError, match="expected_sync_handler"):
        bind_sync(
            "operation",
            "wait",
            handler,
            TypeAdapter(Arguments),
            TypeAdapter(Output),
            None,
            result_property=False,
        )
    with pytest.raises(BindingError, match="expected_async_handler"):
        bind_async(
            "operation",
            "wait",
            lambda args: Output(result=args.value),
            TypeAdapter(Arguments),
            TypeAdapter(Output),
            None,
            result_property=False,
        )
