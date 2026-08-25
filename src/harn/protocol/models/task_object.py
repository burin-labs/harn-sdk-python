from enum import Enum


class TaskObject(str, Enum):
    TASK = "task"

    def __str__(self) -> str:
        return str(self.value)
