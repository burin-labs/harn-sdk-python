from enum import Enum


class ReceiptObject(str, Enum):
    RECEIPT = "receipt"

    def __str__(self) -> str:
        return str(self.value)
