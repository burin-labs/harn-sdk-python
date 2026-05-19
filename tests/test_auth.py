import httpx

from harn.auth import APIKeyCredential, AmbientCredential
from harn.auth import OAuthDeviceFlowCredential


def test_api_key_credential_returns_value() -> None:
    cred = APIKeyCredential("abc")
    assert cred.get_token() == "abc"


def test_ambient_credential_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("HARN_API_KEY", "xyz")
    cred = AmbientCredential()
    assert cred.get_token() == "xyz"


def test_ambient_credential_missing(monkeypatch) -> None:
    monkeypatch.delenv("HARN_API_KEY", raising=False)
    cred = AmbientCredential()
    assert cred.get_token() is None


def test_oauth_device_flow_uses_oidc_discovery_endpoints() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append((request.method, request.url.path, request.read()))
        if request.url.path == "/.well-known/openid-configuration":
            return httpx.Response(
                200,
                json={
                    "device_authorization_endpoint": "https://auth.example.test/oauth/device",
                    "token_endpoint": "https://auth.example.test/oauth/token",
                },
            )
        if request.url.path == "/oauth/device":
            return httpx.Response(
                200,
                json={
                    "device_code": "dev-1",
                    "user_code": "ABCD",
                    "verification_uri": "https://auth.example.test/activate",
                    "expires_in": 300,
                },
            )
        if request.url.path == "/oauth/token":
            return httpx.Response(
                200,
                json={"access_token": "token-1", "token_type": "Bearer"},
            )
        raise AssertionError(request.url)

    cred = OAuthDeviceFlowCredential(
        "https://auth.example.test",
        client_id="client-1",
        scope="tasks:create",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    discovery = cred.discover()
    authorization = cred.start()
    token = cred.poll("dev-1")

    assert discovery["token_endpoint"] == "https://auth.example.test/oauth/token"
    assert authorization["token_endpoint"] == "https://auth.example.test/oauth/token"
    assert token == "token-1"
    assert cred.get_token() == "token-1"
    assert seen == [
        ("GET", "/.well-known/openid-configuration", b""),
        ("POST", "/oauth/device", b"client_id=client-1&scope=tasks%3Acreate"),
        (
            "POST",
            "/oauth/token",
            b"grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code&device_code=dev-1&client_id=client-1",
        ),
    ]


def test_oauth_device_flow_slow_down_extends_poll_interval(monkeypatch) -> None:
    sleeps = []
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(400, json={"error": "slow_down"})
        return httpx.Response(200, json={"access_token": "token-2"})

    monkeypatch.setattr("harn.auth.time.sleep", sleeps.append)
    cred = OAuthDeviceFlowCredential(
        "https://auth.example.test",
        client_id="client-1",
        scope="tasks:create",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    assert cred.poll("dev-1", interval=5, timeout_seconds=300) == "token-2"
    assert sleeps == [10]
