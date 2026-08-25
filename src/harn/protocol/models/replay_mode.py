from enum import Enum


class ReplayMode(str, Enum):
    EXACT = "exact"
    FROM_CHECKPOINT = "from_checkpoint"
    WITH_OVERRIDES = "with_overrides"

    def __str__(self) -> str:
        return str(self.value)
