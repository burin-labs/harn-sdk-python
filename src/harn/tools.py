from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class ToolRegistration:
    name: str
    description: str
    fn: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolRegistration] = {}

    def tool(self, name: str | None = None, description: str = "") -> Callable[[F], F]:
        def decorator(fn: F) -> F:
            tool_name = name or fn.__name__
            self._tools[tool_name] = ToolRegistration(
                name=tool_name,
                description=description or (fn.__doc__ or ""),
                fn=fn,
            )
            return fn

        return decorator

    def list(self) -> list[ToolRegistration]:
        return list(self._tools.values())


registry = ToolRegistry()
tool = registry.tool
