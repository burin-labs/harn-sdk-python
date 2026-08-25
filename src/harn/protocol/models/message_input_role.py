from enum import Enum


class MessageInputRole(str, Enum):
    AGENT = "agent"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
