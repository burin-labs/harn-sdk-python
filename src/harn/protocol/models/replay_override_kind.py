from enum import Enum


class ReplayOverrideKind(str, Enum):
    CHECKPOINT_VALUE = "checkpoint_value"
    EVENT_PAYLOAD = "event_payload"
    HOST_FACT = "host_fact"
    LLM_PROVIDER_RESPONSE = "llm_provider_response"
    MCP_TOOL_RETURN = "mcp_tool_return"
    SECRET_VALUE = "secret_value"
    TIME = "time"
    TOOL_RESULT = "tool_result"

    def __str__(self) -> str:
        return str(self.value)
