from enum import Enum


class QuotaObject(str, Enum):
    QUOTA = "quota"

    def __str__(self) -> str:
        return str(self.value)
