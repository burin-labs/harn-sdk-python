from enum import Enum


class ToolResultPartStatus(str, Enum):
    ERROR = "error"
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
