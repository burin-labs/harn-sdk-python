from enum import Enum


class DiscoveryProtocolFamily(str, Enum):
    HARN_AGENTS_PROTOCOL = "harn_agents_protocol"

    def __str__(self) -> str:
        return str(self.value)
