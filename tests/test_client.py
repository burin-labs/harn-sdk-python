import httpx
import pytest

from harn import HARN_PROTOCOL_VERSION, AsyncHarnClient, HarnClient


def test_client_adds_auth_header() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer token-123"
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com"),
        token="token-123",
    ) as client:
        response = client.get_protocol_discovery()
    assert response == {"ok": True}


def test_client_adds_current_protocol_header_to_v1_calls() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["harn-agents-protocol-version"] == HARN_PROTOCOL_VERSION
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        response = client.list_sessions()
    assert response == {"ok": True}


def test_public_discovery_omits_protocol_header() -> None:
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["has_protocol"] = "harn-agents-protocol-version" in request.headers
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        response = client.get_well_known_agent_card()
    assert response == {"ok": True}
    assert seen["has_protocol"] is False


def test_client_path_params() -> None:
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["path"] = request.url.path
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        client.get_session("sess_1")
    assert seen["path"] == "/v1/sessions/sess_1"


def test_new_cloud_endpoint_helpers_escape_path_segments_and_idempotency() -> None:
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["path"] = request.url.raw_path.decode()
        seen["body"] = request.read()
        seen["idempotency"] = request.headers["idempotency-key"]
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        response = client.review_context_pack_artifact(
            "pack/1",
            "v1",
            "artifact/2",
            body={"decision": "approve"},
            idempotency_key="idem-1",
        )
    assert response == {"ok": True}
    assert seen == {
        "method": "POST",
        "path": "/v1/context-packs/pack%2F1/versions/v1/artifacts/artifact%2F2/review",
        "body": b'{"decision":"approve"}',
        "idempotency": "idem-1",
    }


def test_request_escape_hatch_reaches_unwrapped_cloud_endpoints() -> None:
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["path"] = request.url.path
        seen["query"] = request.url.query.decode()
        return httpx.Response(204)

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        response = client.request(
            "PATCH",
            "/v1/remote-attach/policy",
            params={"enabled": True},
        )
    assert response is None
    assert seen == {
        "method": "PATCH",
        "path": "/v1/remote-attach/policy",
        "query": "enabled=true",
    }


@pytest.mark.asyncio
async def test_async_client_shares_response_and_header_behavior() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["harn-agents-protocol-version"] == HARN_PROTOCOL_VERSION
        return httpx.Response(200, json={"events": []})

    transport = httpx.MockTransport(handler)
    async with AsyncHarnClient(
        client=httpx.AsyncClient(
            transport=transport, base_url="https://api.harnlang.com"
        )
    ) as client:
        response = await client.list_channel_events()
    assert response == {"events": []}
