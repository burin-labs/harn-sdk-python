from enum import Enum


class MemoryScope(str, Enum):
    PERSONA = "persona"
    SESSION = "session"
    TENANT = "tenant"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
