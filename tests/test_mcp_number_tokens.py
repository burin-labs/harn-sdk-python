import json

import httpx
import pytest
from pydantic import StrictInt, TypeAdapter

from harn._base_url import DEFAULT_BASE_URL
from harn._binding_runtime import decode_result
from harn._mcp_client import McpClient
from harn.bindings import BindingError
from harn.client import HarnClient


def response_with(token):
    def respond(request):
        identity = json.loads(request.content)["id"]
        body = (
            '{"jsonrpc":"2.0","id":'
            + json.dumps(identity)
            + ',"result":{"resultType":"complete","isError":false,"structuredContent":'
            + token
            + "}}"
        )
        return httpx.Response(
            200, content=body, headers={"content-type": "application/json"}
        )

    return respond


def test_mcp_transport_keeps_negative_zero_distinct_from_an_integer_token():
    for token, valid in [("1", True), ("-0", False), ("1.0", False)]:
        http = httpx.Client(
            base_url=DEFAULT_BASE_URL,
            transport=httpx.MockTransport(response_with(token)),
        )
        with HarnClient(token="synthetic", client=http) as client:
            result = McpClient(client).rpc(
                "tools/call", {"name": "number", "arguments": {}}
            )
            if valid:
                assert (
                    decode_result(
                        "number",
                        result,
                        TypeAdapter(StrictInt),
                        None,
                        result_property=False,
                    )
                    == 1
                )
            else:
                with pytest.raises(BindingError, match="invalid_wire_value"):
                    decode_result(
                        "number",
                        result,
                        TypeAdapter(StrictInt),
                        None,
                        result_property=False,
                    )
