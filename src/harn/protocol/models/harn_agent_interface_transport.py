from enum import Enum


class HarnAgentInterfaceTransport(str, Enum):
    A2A = "a2a"
    ACP = "acp"
    MCP = "mcp"
    REST = "rest"
    SSE = "sse"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
