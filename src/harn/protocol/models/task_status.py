from enum import Enum


class TaskStatus(str, Enum):
    AUTH_REQUIRED = "AUTH_REQUIRED"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    INPUT_REQUIRED = "INPUT_REQUIRED"
    SUBMITTED = "SUBMITTED"
    WORKING = "WORKING"

    def __str__(self) -> str:
        return str(self.value)
