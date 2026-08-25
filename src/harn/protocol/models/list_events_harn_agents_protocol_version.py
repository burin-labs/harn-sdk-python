from enum import Enum


class ListEventsHarnAgentsProtocolVersion(str, Enum):
    AGENTS_PROTOCOL_2026_04_25 = "agents-protocol-2026-04-25"

    def __str__(self) -> str:
        return str(self.value)
