from enum import Enum


class RuntimeMetadataObject(str, Enum):
    RUNTIME = "runtime"

    def __str__(self) -> str:
        return str(self.value)
