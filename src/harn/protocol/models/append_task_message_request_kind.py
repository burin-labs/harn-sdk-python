from enum import Enum


class AppendTaskMessageRequestKind(str, Enum):
    INPUT = "input"

    def __str__(self) -> str:
        return str(self.value)
