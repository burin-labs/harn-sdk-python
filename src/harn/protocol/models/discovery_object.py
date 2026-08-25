from enum import Enum


class DiscoveryObject(str, Enum):
    PROTOCOL_DISCOVERY = "protocol_discovery"

    def __str__(self) -> str:
        return str(self.value)
