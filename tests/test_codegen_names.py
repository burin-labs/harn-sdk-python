import pytest

from harn._codegen.names import Symbol, allocate, identifier


def test_collision_names_are_stable_when_declarations_are_reordered() -> None:
    symbols = [
        Symbol("first", "a-b"),
        Symbol("second", "a_b"),
        Symbol("third", "class"),
    ]
    result = allocate(symbols)
    assert result == allocate(reversed(symbols))
    assert len(set(result.values())) == 3
    assert result["third"] == "class_"
    assert result["first"].startswith("a_b_")
    assert result["second"].startswith("a_b_")


def test_duplicate_semantic_ids_fail_instead_of_overwriting() -> None:
    with pytest.raises(ValueError, match="duplicate semantic"):
        allocate([Symbol("same", "first"), Symbol("same", "second")])


def test_generated_api_and_pydantic_names_remain_available() -> None:
    symbols = [
        Symbol("one", "model_dump"),
        Symbol("two", "dict"),
        Symbol("three", "Client"),
    ]
    result = allocate(symbols, reserved=frozenset({"Client"}))
    assert result["one"] == "field_model_dump"
    assert result["two"] == "field_dict"
    assert result["three"] != "Client"
    assert identifier("type") == "type_"


@pytest.mark.parametrize("value", ["", "λ", "123", "__init__", "async", "a/b", "a.b"])
def test_allocated_names_are_real_python_identifiers(value: str) -> None:
    assert identifier(value).isascii()
    assert identifier(value).isidentifier()
