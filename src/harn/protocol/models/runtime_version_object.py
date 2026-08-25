from enum import Enum


class RuntimeVersionObject(str, Enum):
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)
