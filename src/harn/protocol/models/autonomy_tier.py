from enum import Enum


class AutonomyTier(str, Enum):
    ACT_AUTO = "act_auto"
    ACT_WITH_APPROVAL = "act_with_approval"
    SHADOW = "shadow"
    SUGGEST = "suggest"

    def __str__(self) -> str:
        return str(self.value)
