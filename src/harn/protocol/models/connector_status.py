from enum import Enum


class ConnectorStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"

    def __str__(self) -> str:
        return str(self.value)
