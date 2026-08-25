from enum import Enum


class TruncateSessionHarnAgentsProtocolVersion(str, Enum):
    AGENTS_PROTOCOL_2026_04_25 = "agents-protocol-2026-04-25"

    def __str__(self) -> str:
        return str(self.value)
