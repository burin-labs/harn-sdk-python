from __future__ import annotations

import httpx
import pytest
from fastapi.testclient import TestClient

from examples.fastapi_provider_catalog import create_app
from harn import create_harn_protocol_client
from harn.protocol.api.runtime import get_health


def test_generated_provider_catalog_in_existing_fastapi_route() -> None:
    seen: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200,
            json={
                "schema_version": 6,
                "schema": "https://harnlang.com/schemas/provider-catalog.v6.json",
                "generated_by": "test",
                "providers": [],
                "models": [],
                "aliases": [],
                "variants": [],
                "families": [],
                "qc_defaults": {},
            },
        )

    with pytest.warns(UserWarning, match="base_url overridden"):
        client = create_harn_protocol_client(
            base_url="https://example.test",
            token="test-token",
            transport=httpx.MockTransport(handle),
        )

    response = TestClient(create_app(client)).get("/models")

    assert response.status_code == 200
    assert response.json()["schema_version"] == 6
    assert len(seen) == 1
    assert str(seen[0].url) == "https://example.test/v1/provider-catalog"
    assert seen[0].headers["authorization"] == "Bearer test-token"
    assert (
        seen[0].headers["harn-agents-protocol-version"] == "agents-protocol-2026-04-25"
    )


def test_generated_public_discovery_omits_bearer() -> None:
    seen: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200,
            json={"ok": True, "status": "ready", "version": "0.10.116"},
        )

    client = create_harn_protocol_client(
        token="test-token",
        transport=httpx.MockTransport(handle),
    )
    health = get_health.sync(client=client)

    assert health is not None
    assert health.ok is True
    assert "authorization" not in seen[0].headers
    assert "harn-agents-protocol-version" not in seen[0].headers
