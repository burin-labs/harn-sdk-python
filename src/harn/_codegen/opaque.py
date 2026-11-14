"""Opaque JSON projections: these are forwarded, never interpreted as Harn types."""

from typing import TypeAlias

from pydantic import JsonValue

JsonArray: TypeAlias = list[JsonValue]
