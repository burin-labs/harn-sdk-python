"""Tests for the 2026-05-23 security sweep:

* F1 cross-host bearer leak guard
* F2 AmbientCredential opt-in (no auto-fallback)
* F8 stream_artifact_content
* F9 https-only base_url
"""

from __future__ import annotations

import warnings

import httpx
import pytest

from harn import AmbientCredential, AsyncHarnClient, HarnClient


# ---------------------------------------------------------------------------
# F1 — host-pinned bearer
# ---------------------------------------------------------------------------


def test_host_pin_attaches_token_for_configured_host() -> None:
    seen: dict[str, str | None] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers.get("authorization")
        return httpx.Response(
            200, json={"object": "session_list", "data": [], "has_more": False}
        )

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com"),
        token="token-pinned",
    ) as client:
        # list_sessions is auth=True (not public), so the bearer must be sent
        client.list_sessions()

    assert seen["auth"] == "Bearer token-pinned"


def test_host_pin_drops_token_for_cross_host_absolute_url() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with HarnClient(
            client=httpx.Client(transport=transport, base_url="https://example.test"),
            base_url="https://example.test",
            token="token-pinned",
        ) as client:
            # Issue a request whose absolute path points to a different host
            # than the configured base_url. The bearer must NOT travel along.
            client.request("GET", "https://attacker.example/leak")

    assert captured, "request was never made"
    assert captured[0].url.host == "attacker.example"
    assert "authorization" not in {k.lower() for k in captured[0].headers.keys()}


def test_warning_when_base_url_overridden_with_token() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        HarnClient(base_url="https://localhost-dev.test", token="token")
    messages = [str(w.message) for w in caught if issubclass(w.category, UserWarning)]
    assert any("base_url overridden" in m for m in messages), messages


def test_no_warning_for_default_base_url() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        HarnClient(token="token")
    user_warnings = [w for w in caught if issubclass(w.category, UserWarning)]
    assert not user_warnings, [str(w.message) for w in user_warnings]


# ---------------------------------------------------------------------------
# F2 — AmbientCredential is opt-in only
# ---------------------------------------------------------------------------


def test_no_auto_ambient_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HARN_API_KEY", "env-only-key")
    seen: dict[str, str | None] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers.get("authorization")
        return httpx.Response(
            200, json={"object": "session_list", "data": [], "has_more": False}
        )

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        # list_sessions requires auth — if AmbientCredential were applied
        # implicitly, the env var would land in Authorization here.
        client.list_sessions()

    assert seen["auth"] is None, "ambient HARN_API_KEY must not be picked up implicitly"


def test_explicit_ambient_credential_opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HARN_API_KEY", "env-key-opted-in")
    seen: dict[str, str | None] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers.get("authorization")
        return httpx.Response(
            200, json={"object": "session_list", "data": [], "has_more": False}
        )

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com"),
        credential=AmbientCredential(),
    ) as client:
        client.list_sessions()

    assert seen["auth"] == "Bearer env-key-opted-in"


# ---------------------------------------------------------------------------
# F8 — stream_artifact_content yields chunks
# ---------------------------------------------------------------------------


def test_stream_artifact_content_yields_chunks() -> None:
    payload = b"abc" * 1024

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=payload,
            headers={"content-type": "application/octet-stream"},
        )

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com"),
        token="token",
    ) as client:
        chunks = b"".join(client.stream_artifact_content("art_1"))
    assert chunks == payload


def test_download_artifact_content_emits_deprecation() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, content=b"data", headers={"content-type": "application/octet-stream"}
        )

    transport = httpx.MockTransport(handler)
    with (
        HarnClient(
            client=httpx.Client(
                transport=transport, base_url="https://api.harnlang.com"
            ),
            token="token",
        ) as client,
        warnings.catch_warnings(record=True) as caught,
    ):
        warnings.simplefilter("always")
        client.download_artifact_content("art_1")

    deprecations = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert deprecations, "download_artifact_content should emit DeprecationWarning"


# ---------------------------------------------------------------------------
# F9 — https-only base_url
# ---------------------------------------------------------------------------


def test_base_url_rejects_plain_http() -> None:
    with pytest.raises(ValueError, match="https://"):
        HarnClient(base_url="http://api.attacker.example")


def test_base_url_allows_http_localhost() -> None:
    # No exception, no warning required (user opted into local dev).
    client = HarnClient(base_url="http://localhost:8080")
    client.close()


def test_base_url_allows_http_127() -> None:
    client = HarnClient(base_url="http://127.0.0.1:8080")
    client.close()


def test_base_url_rejects_unknown_scheme() -> None:
    with pytest.raises(ValueError):
        HarnClient(base_url="ftp://api.harnlang.com")


# ---------------------------------------------------------------------------
# F1 — async path-host pin (smoke)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_host_pin_drops_token_for_cross_host() -> None:
    captured: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        async with AsyncHarnClient(
            client=httpx.AsyncClient(
                transport=transport, base_url="https://example.test"
            ),
            base_url="https://example.test",
            token="token-pinned",
        ) as client:
            await client.request("GET", "https://attacker.example/leak")

    assert captured, "request was never made"
    assert captured[0].url.host == "attacker.example"
    assert "authorization" not in {k.lower() for k in captured[0].headers.keys()}
