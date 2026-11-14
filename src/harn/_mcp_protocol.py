"""Stable MCP request projection shared by synchronous and asynchronous clients."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import version
from typing import Literal

from mcp.shared.inbound import encode_header_value
from pydantic import MISSING, JsonValue

from ._codegen import protocol as facts
from .bindings import BindingError, WireModel


@dataclass(frozen=True)
class McpHeaders:
    method: str
    subject: str | None = None

    @classmethod
    def for_request(cls, method: str, params: dict[str, JsonValue]) -> McpHeaders:
        field = facts.MCP_NAME_FIELDS.get(method)
        if field is None:
            return cls(method)
        subject = params.get(field)
        if not isinstance(subject, str) or not subject:
            raise BindingError("mcp_subject_unmeasured", method)
        return cls(method, subject)

    def fields(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            facts.MCP_HEADER_METHOD: self.method,
            facts.MCP_HEADER_PROTOCOL_VERSION: facts.MCP_PROTOCOL_VERSION,
        }
        if self.subject is not None:
            headers[facts.MCP_HEADER_NAME] = encode_header_value(self.subject)
        return headers


def request_params(params: dict[str, JsonValue]) -> dict[str, JsonValue]:
    metadata: dict[str, JsonValue] = {
        facts.MCP_META_KEY_PROTOCOL_VERSION: facts.MCP_PROTOCOL_VERSION,
        facts.MCP_META_KEY_CLIENT_INFO: {
            "name": "harn-sdk-python",
            "version": version("harn-sdk"),
        },
        facts.MCP_META_KEY_CLIENT_CAPABILITIES: {
            "extensions": {facts.MCP_TASKS_EXTENSION_ID: {}}
        },
    }
    result = dict(params)
    result["_meta"] = metadata
    return result


class JsonRpcError(WireModel):
    code: int
    message: str
    data: JsonValue | MISSING = MISSING


class JsonRpcResponse(WireModel):
    jsonrpc: Literal["2.0"]
    id: str
    result: JsonValue | MISSING = MISSING
    error: JsonRpcError | MISSING = MISSING


def response_result(raw: JsonValue, identity: str, method: str) -> JsonValue:
    response = JsonRpcResponse.model_validate(raw)
    if response.id != identity:
        raise BindingError("mcp_response_identity", method)
    if response.result is not MISSING and response.error is not MISSING:
        raise BindingError("mcp_response_ambiguous", method)
    if response.error is not MISSING:
        raise BindingError(f"mcp_rpc_error:{response.error.code}", method)
    if response.result is MISSING:
        raise BindingError("mcp_response_missing_result", method)
    return response.result


def discovery_result(result: dict[str, JsonValue]) -> None:
    versions = result.get("supportedVersions")
    capabilities = result.get("capabilities")
    if (
        result.get("resultType") != "complete"
        or not isinstance(versions, list)
        or not versions
        or not all(isinstance(item, str) for item in versions)
        or facts.MCP_PROTOCOL_VERSION not in versions
    ):
        raise BindingError("mcp_protocol_unavailable")
    if not isinstance(capabilities, dict) or not isinstance(
        capabilities.get("tools"), dict
    ):
        raise BindingError("mcp_tools_unavailable")
