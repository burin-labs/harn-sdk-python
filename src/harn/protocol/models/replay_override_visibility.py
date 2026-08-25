from enum import Enum


class ReplayOverrideVisibility(str, Enum):
    INTERNAL = "internal"
    PUBLIC = "public"
    RECEIPT_ONLY = "receipt_only"

    def __str__(self) -> str:
        return str(self.value)
