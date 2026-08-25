from enum import Enum


class PermissionRequestSource(str, Enum):
    ACP = "acp"
    HITL = "hitl"

    def __str__(self) -> str:
        return str(self.value)
