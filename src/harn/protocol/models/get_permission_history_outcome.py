from enum import Enum


class GetPermissionHistoryOutcome(str, Enum):
    DENIED = "denied"
    ESCALATED = "escalated"
    GRANTED = "granted"

    def __str__(self) -> str:
        return str(self.value)
