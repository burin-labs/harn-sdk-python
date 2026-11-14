# Generated from Harn harn-codegen-protocol.json. Do not edit.
from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

HARN_MCP_TOOL_CONTRACT_META_KEY: Final = "com.harnlang/toolContract"
HARN_NATIVE_BINDING_META_KEY: Final = "com.harnlang/nativeBinding"
MCP_HEADER_METHOD: Final = "Mcp-Method"
MCP_HEADER_NAME: Final = "Mcp-Name"
MCP_HEADER_PROTOCOL_VERSION: Final = "MCP-Protocol-Version"
MCP_HEADER_VALUE_ENCODING: Final = MappingProxyType(
    {"plain_maximum": 126, "plain_minimum": 32, "prefix": "=?base64?", "suffix": "?="}
)
MCP_HEADER_VALUE_EXAMPLES: Final = (
    MappingProxyType({"encoded": "echo", "value": "echo"}),
    MappingProxyType({"encoded": "=?base64?zpTOv866zrnOvM6u?=", "value": "Δοκιμή"}),
    MappingProxyType({"encoded": "=?base64?IHBhZGRlZCA=?=", "value": " padded "}),
    MappingProxyType(
        {"encoded": "=?base64?bGluZTEKbGluZTI=?=", "value": "line1\nline2"}
    ),
    MappingProxyType(
        {
            "encoded": "=?base64?PT9iYXNlNjQ/bGl0ZXJhbD89?=",
            "value": "=?base64?literal?=",
        }
    ),
    MappingProxyType({"encoded": "=?base64?YQli?=", "value": "a\tb"}),
    MappingProxyType({"encoded": "", "value": ""}),
)
MCP_MAX_STDIO_LINE_BYTES: Final = 16777216
MCP_META_KEY_CLIENT_CAPABILITIES: Final = "io.modelcontextprotocol/clientCapabilities"
MCP_META_KEY_CLIENT_INFO: Final = "io.modelcontextprotocol/clientInfo"
MCP_META_KEY_PROTOCOL_VERSION: Final = "io.modelcontextprotocol/protocolVersion"
MCP_META_KEY_SERVER_INFO: Final = "io.modelcontextprotocol/serverInfo"
MCP_METHOD_CANCELLED_NOTIFICATION: Final = "notifications/cancelled"
MCP_METHOD_SERVER_DISCOVER: Final = "server/discover"
MCP_METHOD_TASKS_CANCEL: Final = "tasks/cancel"
MCP_METHOD_TASKS_GET: Final = "tasks/get"
MCP_METHOD_TOOLS_CALL: Final = "tools/call"
MCP_METHOD_TOOLS_LIST: Final = "tools/list"
MCP_NAME_FIELDS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "prompts/get": "name",
        "resources/read": "uri",
        "tasks/cancel": "taskId",
        "tasks/get": "taskId",
        "tasks/update": "taskId",
        "tools/call": "name",
    }
)
MCP_PROTOCOL_VERSION: Final = "2026-07-28"
MCP_STDIO_LINE_LIMIT_INCLUDES_TERMINATOR: Final = True
MCP_TASKS_EXTENSION_ID: Final = "io.modelcontextprotocol/tasks"
NATIVE_MCP_BINDING_VERSION: Final = "harn-tools-mcp/1.0"
WIRE_BYTES_TAG: Final = "$bytes_b64"
WIRE_DECIMAL_MAX_MANTISSA: Final = "79228162514264337593543950335"
WIRE_DECIMAL_MAX_SCALE: Final = 28
WIRE_DECIMAL_PATTERN: Final = "^-?(0|[1-9][0-9]*)(\\.[0-9]{1,28})?$"
WIRE_DECIMAL_PRESERVES_NEGATIVE_ZERO: Final = False
WIRE_DECIMAL_PRESERVES_SCALE: Final = True
WIRE_ENUM_FIELDS_KEY: Final = "fields"
WIRE_ENUM_NAME_KEY: Final = "enum"
WIRE_ENUM_VARIANT_KEY: Final = "variant"
WIRE_INTEGER_TOKEN_PATTERN: Final = "^(0|-?[1-9][0-9]*)$"
WIRE_MAX_VALUE_DEPTH: Final = 128
