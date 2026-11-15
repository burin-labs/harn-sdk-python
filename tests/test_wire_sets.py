import json
from decimal import Decimal
from typing import ClassVar, Literal

import pytest
from pydantic import Field, StrictBool, StrictInt, TypeAdapter, ValidationError

from harn._wire_sets import _equal
from harn.bindings import WireDecimal, WireModel, WireSet


def test_ordered_set_arrays_keep_boolean_and_integer_members_distinct():
    adapter = TypeAdapter(WireSet[StrictBool | StrictInt])
    value = adapter.validate_json("[true,1,false,0]", strict=True)
    assert [type(member) for member in value] == [bool, int, bool, int]
    assert adapter.dump_json(value) == b"[true,1,false,0]"
    with pytest.raises(ValidationError):
        adapter.validate_json("[true,1,true]", strict=True)


def test_decimal_duplicate_equality_ignores_scale_but_not_numeric_type():
    with pytest.raises(ValidationError):
        TypeAdapter(WireSet[WireDecimal]).validate_json('["1.0","1.00"]', strict=True)
    adapter = TypeAdapter(WireSet[WireDecimal | StrictInt])
    value = adapter.validate_json('["1.00",1]', strict=True)
    assert type(value[0]) is Decimal and type(value[1]) is int
    assert adapter.dump_json(value) == b'["1.00",1]'


class Record(WireModel):
    name: str
    values: list[StrictInt]


def test_record_members_compare_by_fields_without_hash_or_reference_identity():
    adapter = TypeAdapter(WireSet[Record])
    positive = adapter.validate_json(
        '[{"name":"a","values":[1]},{"name":"b","values":[1]}]', strict=True
    )
    assert len(positive) == 2
    with pytest.raises(ValidationError):
        adapter.validate_json(
            '[{"name":"a","values":[1]},{"values":[1],"name":"a"}]', strict=True
        )
    first = Record(name="a", values=[1])
    second = Record(name="a", values=[1])
    assert first is not second
    with pytest.raises(ValueError, match="duplicate wire set member"):
        WireSet([first, second])


def test_nested_set_members_are_unordered_but_preserve_first_occurrence_order():
    adapter = TypeAdapter(WireSet[WireSet[StrictInt]])
    value = adapter.validate_json("[[2,1],[3]]", strict=True)
    assert adapter.dump_json(value) == b"[[2,1],[3]]"
    with pytest.raises(ValidationError):
        adapter.validate_json("[[2,1],[1,2]]", strict=True)


def test_mutated_native_members_are_revalidated_before_encoding():
    adapter = TypeAdapter(WireSet[Record])
    values = adapter.validate_python(
        WireSet([Record(name="a", values=[1]), Record(name="b", values=[1])]),
        strict=True,
    )
    values[1].name = "a"
    with pytest.raises(ValidationError):
        adapter.validate_python(values, strict=True)


def test_reserved_payload_keys_do_not_turn_a_record_into_a_nominal_enum():
    class ReservedRecord(WireModel):
        enum_name: Literal["Mode"] = Field(
            validation_alias="enum", serialization_alias="enum"
        )
        variant: Literal["One"]
        fields: tuple[StrictInt]

    class Variant(ReservedRecord):
        __harn_wire_kind__: ClassVar[Literal["record", "enum"]] = "enum"

    record = ReservedRecord(enum_name="Mode", variant="One", fields=(1,))
    variant = Variant(enum_name="Mode", variant="One", fields=(1,))
    assert record.model_dump(by_alias=True) == variant.model_dump(by_alias=True)
    assert not _equal(record, variant)
    assert _equal(variant, Variant(enum_name="Mode", variant="One", fields=(1,)))


def test_nominal_records_compare_the_harn_name_in_addition_to_fields():
    class First(Record):
        __harn_nominal_name__: ClassVar[str | None] = "First"

    class Second(Record):
        __harn_nominal_name__: ClassVar[str | None] = "Second"

    assert not _equal(First(name="a", values=[1]), Second(name="a", values=[1]))
    assert not _equal(First(name="a", values=[1]), {"name": "a", "values": [1]})
    assert _equal(Record(name="a", values=[1]), {"values": [1], "name": "a"})


def test_mixed_numeric_comparison_uses_harn_float_conversion():
    assert _equal(9007199254740993, 9007199254740992.0)
    assert not _equal(9007199254740993, 9007199254740992)
    assert not _equal(Decimal("1.0"), 1)


def test_set_validation_refuses_cyclic_untyped_values_without_recursion_crash():
    cycle = []
    cycle.append(cycle)
    with pytest.raises(ValueError, match="wire value depth exceeded"):
        WireSet([cycle])


def test_empty_set_is_a_known_array_shape_and_input_duplicates_are_never_dropped():
    adapter = TypeAdapter(WireSet[StrictInt])
    assert json.loads(adapter.dump_json(adapter.validate_json("[]", strict=True))) == []
    with pytest.raises(ValidationError):
        adapter.validate_json("[1,1]", strict=True)


def test_native_set_is_immutable_and_membership_uses_harn_equality():
    boolean = WireSet([True])
    assert True in boolean
    assert 1 not in boolean
    assert WireSet([1, 2]) == WireSet([2, 1])
    with pytest.raises(AttributeError):
        boolean._values = (False,)
    with pytest.raises(TypeError):
        hash(boolean)


def test_enum_discriminator_envelope_does_not_consume_semantic_value_depth():
    class RecursiveVariant(WireModel):
        __harn_wire_kind__: ClassVar[Literal["record", "enum"]] = "enum"
        enum_name: Literal["Tree"] = Field(serialization_alias="enum")
        variant: Literal["Next"]
        fields: tuple["RecursiveVariant | None"]

    RecursiveVariant.model_rebuild()
    value = None
    for _ in range(100):
        value = RecursiveVariant.model_construct(
            enum_name="Tree", variant="Next", fields=(value,)
        )
    assert len(WireSet([value])) == 1
