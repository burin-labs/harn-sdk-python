from enum import Enum


class PermissionDecisionDeniedOutcome(str, Enum):
    DENIED = "denied"

    def __str__(self) -> str:
        return str(self.value)
