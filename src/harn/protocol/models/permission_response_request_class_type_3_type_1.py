from enum import Enum


class PermissionResponseRequestClassType3Type1(str, Enum):
    CUSTOM = "custom"
    EXEC = "exec"
    LLM = "llm"
    NET = "net"
    READ = "read"
    WRITE = "write"

    def __str__(self) -> str:
        return str(self.value)
