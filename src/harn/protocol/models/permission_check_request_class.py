from enum import Enum


class PermissionCheckRequestClass(str, Enum):
    CUSTOM = "custom"
    EXEC = "exec"
    LLM = "llm"
    NET = "net"
    READ = "read"
    WRITE = "write"

    def __str__(self) -> str:
        return str(self.value)
