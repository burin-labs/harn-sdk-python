from enum import Enum


class BranchKind(str, Enum):
    SANDBOX = "sandbox"
    SESSION = "session"
    TASK = "task"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
