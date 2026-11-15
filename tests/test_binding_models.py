from typing import Annotated, Literal

import pytest
from pydantic import MISSING, BeforeValidator, TypeAdapter, ValidationError

from harn.bindings import ApplicationFailure, WireModel, wire_literal_validator


class Payload(WireModel):
    required: str
    optional: str | MISSING = MISSING
    nullable: str | None


def test_integer_and_boolean_literals_do_not_coerce_into_each_other() -> None:
    integer = TypeAdapter(
        Annotated[Literal[1], BeforeValidator(wire_literal_validator(1))]
    )
    boolean = TypeAdapter(
        Annotated[Literal[True], BeforeValidator(wire_literal_validator(True))]
    )
    assert integer.validate_json("1", strict=True) == 1
    assert boolean.validate_json("true", strict=True) is True
    with pytest.raises(ValidationError):
        integer.validate_json("true", strict=True)
    with pytest.raises(ValidationError):
        boolean.validate_json("1", strict=True)


def test_omitted_and_explicitly_null_fields_are_distinct() -> None:
    payload = Payload(required="ok", nullable=None)
    assert payload.optional is MISSING
    assert payload.model_dump(mode="json") == {"required": "ok", "nullable": None}
    assert (
        Payload.model_validate_json('{"required":"ok","nullable":null}').optional
        is MISSING
    )
    with pytest.raises(ValidationError):
        Payload.model_validate_json('{"required":"ok","nullable":null,"optional":null}')
    with pytest.raises(ValidationError):
        Payload.model_validate_json('{"required":"ok"}')


def test_constructed_or_mutated_invalid_models_cannot_become_success() -> None:
    adapter = TypeAdapter(Payload)
    with pytest.raises(ValidationError):
        adapter.validate_python(Payload.model_construct(required=42, nullable=None))
    payload = Payload(required="ok", nullable=None)
    with pytest.raises(ValidationError):
        payload.required = 42
    with pytest.raises(ValidationError):
        Payload.model_validate_json('{"required":"ok","nullable":null,"extra":true}')


def test_declared_failure_revalidates_its_typed_data() -> None:
    adapter = TypeAdapter(ApplicationFailure[Payload])
    failure = ApplicationFailure[Payload](error=Payload(required="ok", nullable=None))
    assert adapter.validate_python(failure).error.required == "ok"
    with pytest.raises(ValidationError):
        adapter.validate_python(
            ApplicationFailure.model_construct(error={"required": 42})
        )
