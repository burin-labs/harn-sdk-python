from enum import Enum


class SessionState(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    FAILED = "FAILED"
    IDLE = "IDLE"
    PAUSED = "PAUSED"

    def __str__(self) -> str:
        return str(self.value)
