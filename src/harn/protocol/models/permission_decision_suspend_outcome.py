from enum import Enum


class PermissionDecisionSuspendOutcome(str, Enum):
    SUSPEND = "suspend"

    def __str__(self) -> str:
        return str(self.value)
