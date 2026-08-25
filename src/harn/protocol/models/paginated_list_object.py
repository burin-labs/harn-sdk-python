from enum import Enum


class PaginatedListObject(str, Enum):
    LIST = "list"

    def __str__(self) -> str:
        return str(self.value)
