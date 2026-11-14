"""Allocate Python symbols from stable semantic identities, independently of input order."""

from __future__ import annotations

import hashlib
import keyword
import re
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Symbol:
    identity: str
    name: str


def identifier(name: str) -> str:
    """Use ASCII names so the output does not depend on Unicode identifier versions."""
    value = re.sub(r"[^a-zA-Z0-9_]", "_", name).strip("_") or "value"
    if value[0].isdigit():
        value = "value_" + value
    if keyword.iskeyword(value) or value in {"match", "case", "type"}:
        value += "_"
    # Pydantic model APIs and generated private members must remain addressable.
    if value.startswith("model_") or value in {
        "copy",
        "dict",
        "json",
        "schema",
        "schema_json",
        "validate",
        "construct",
        "parse_obj",
        "parse_raw",
        "parse_file",
        "from_orm",
        "update_forward_refs",
    }:
        value = "field_" + value
    return value


def allocate(
    symbols: Iterable[Symbol], *, reserved: frozenset[str] = frozenset()
) -> dict[str, str]:
    ordered = sorted(symbols, key=lambda symbol: symbol.identity)
    identities = [symbol.identity for symbol in ordered]
    if any(not identity for identity in identities) or len(identities) != len(
        set(identities)
    ):
        raise ValueError("empty or duplicate semantic symbol identity")
    candidates = {symbol.identity: identifier(symbol.name) for symbol in ordered}
    counts = Counter(candidates.values())
    result = {
        identity: (
            f"{candidate}_{hashlib.sha256(identity.encode()).hexdigest()}"
            if counts[candidate] > 1 or candidate in reserved
            else candidate
        )
        for identity, candidate in candidates.items()
    }
    if len(set(result.values())) != len(result) or set(result.values()) & reserved:
        raise ValueError("Python symbol collision after semantic identity allocation")
    return result
