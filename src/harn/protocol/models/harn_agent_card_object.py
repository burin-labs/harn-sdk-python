from enum import Enum


class HarnAgentCardObject(str, Enum):
    HARN_AGENT_CARD = "harn_agent_card"

    def __str__(self) -> str:
        return str(self.value)
