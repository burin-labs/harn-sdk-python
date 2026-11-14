"""Harn owns subject selection; the official MCP library owns header encoding."""

import httpx
import pytest
from mcp.shared.inbound import decode_header_value, encode_header_value

from harn._codegen import protocol as facts
from harn._mcp_protocol import McpHeaders
from harn.bindings import BindingError


def test_official_codec_matches_all_mechanically_generated_harn_vectors():
    assert len(facts.MCP_HEADER_VALUE_EXAMPLES) == 7
    assert facts.MCP_STDIO_LINE_LIMIT_INCLUDES_TERMINATOR is True
    for case in facts.MCP_HEADER_VALUE_EXAMPLES:
        assert encode_header_value(case["value"]) == case["encoded"]
        assert decode_header_value(case["encoded"]) == case["value"]


def test_all_six_measured_name_fields_and_unknown_method():
    assert len(facts.MCP_NAME_FIELDS) == 6
    for method, field in facts.MCP_NAME_FIELDS.items():
        headers = McpHeaders.for_request(method, {field: "measured-subject"}).fields()
        assert headers[facts.MCP_HEADER_NAME] == "measured-subject"
        for malformed in ({}, {field: None}, {field: 1}, {field: ""}):
            with pytest.raises(BindingError, match="mcp_subject_unmeasured"):
                McpHeaders.for_request(method, malformed)
    assert (
        facts.MCP_HEADER_NAME
        not in McpHeaders.for_request(
            "unknown/method", {"name": "not-a-standard-subject"}
        ).fields()
    )


@pytest.mark.parametrize(
    "subject",
    ["Δοκιμή", " padded ", "line1\nline2", "=?base64?literal?=", "snow-雪", "plain"],
)
def test_official_sentinel_encoding_survives_actual_httpx_header_construction(subject):
    fields = McpHeaders.for_request(
        facts.MCP_METHOD_TOOLS_CALL, {"name": subject}
    ).fields()
    headers = httpx.Headers(fields)
    assert decode_header_value(headers[facts.MCP_HEADER_NAME]) == subject
    assert (
        headers[facts.MCP_HEADER_NAME] == "plain"
        if subject == "plain"
        else headers[facts.MCP_HEADER_NAME].startswith("=?base64?")
    )
