from enum import Enum


class OutcomeObject(str, Enum):
    OUTCOME = "outcome"

    def __str__(self) -> str:
        return str(self.value)
