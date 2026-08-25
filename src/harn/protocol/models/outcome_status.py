from enum import Enum


class OutcomeStatus(str, Enum):
    CANCELED = "CANCELED"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"

    def __str__(self) -> str:
        return str(self.value)
