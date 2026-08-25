from enum import Enum


class PermissionDecisionGrantedOutcome(str, Enum):
    GRANTED = "granted"

    def __str__(self) -> str:
        return str(self.value)
