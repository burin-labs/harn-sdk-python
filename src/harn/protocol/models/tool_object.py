from enum import Enum


class ToolObject(str, Enum):
    TOOL = "tool"

    def __str__(self) -> str:
        return str(self.value)
