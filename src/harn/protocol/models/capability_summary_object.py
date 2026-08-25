from enum import Enum


class CapabilitySummaryObject(str, Enum):
    CAPABILITY_SUMMARY = "capability_summary"

    def __str__(self) -> str:
        return str(self.value)
