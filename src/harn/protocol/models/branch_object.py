from enum import Enum


class BranchObject(str, Enum):
    BRANCH = "branch"

    def __str__(self) -> str:
        return str(self.value)
