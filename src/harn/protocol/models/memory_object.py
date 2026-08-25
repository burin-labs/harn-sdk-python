from enum import Enum


class MemoryObject(str, Enum):
    MEMORY = "memory"

    def __str__(self) -> str:
        return str(self.value)
