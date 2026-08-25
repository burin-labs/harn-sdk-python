from enum import Enum


class WorkspaceFileEncoding(str, Enum):
    UTF_8 = "utf-8"

    def __str__(self) -> str:
        return str(self.value)
