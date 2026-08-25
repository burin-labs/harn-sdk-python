from enum import Enum


class AuditEntryOutcome(str, Enum):
    DENIED = "denied"
    ESCALATED = "escalated"
    GRANTED = "granted"

    def __str__(self) -> str:
        return str(self.value)
