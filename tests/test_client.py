import httpx

from harn import HarnClient


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
