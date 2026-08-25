from __future__ import annotations

from collections.abc import Generator

import httpx

from ._base_url import (
    DEFAULT_BASE_URL,
    validate_base_url,
    warn_for_authenticated_custom_base_url,
)
from .auth import CredentialProvider
from .protocol.client import Client as ProtocolClient

_PUBLIC_PATHS = frozenset(
    {"/health", "/version", "/openapi.json", "/v1", "/v1/agent-card"}
)


class _HarnBearerAuth(httpx.Auth):
    def __init__(
        self,
        base_host: str,
        token: str | None,
        credential: CredentialProvider | None,
    ) -> None:
        self._base_host = base_host
        self._token = token
        self._credential = credential

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        token = self._token
        if token is None and self._credential is not None:
            token = self._credential.get_token()
        if (
            token
            and request.url.host == self._base_host
            and request.url.path not in _PUBLIC_PATHS
        ):
            request.headers["Authorization"] = f"Bearer {token}"
        yield request


def create_harn_protocol_client(
    *,
    base_url: str = DEFAULT_BASE_URL,
    token: str | None = None,
    credential: CredentialProvider | None = None,
    timeout: float = 30.0,
    transport: httpx.BaseTransport | httpx.AsyncBaseTransport | None = None,
) -> ProtocolClient:
    """Create the transport used by every generated, typed protocol operation."""
    normalized, host = validate_base_url(base_url)
    warn_for_authenticated_custom_base_url(
        normalized,
        authenticated=token is not None or credential is not None,
        stacklevel=2,
    )
    httpx_args: dict[str, object] = {
        "auth": _HarnBearerAuth(host, token, credential),
    }
    if transport is not None:
        httpx_args["transport"] = transport
    return ProtocolClient(
        base_url=normalized,
        timeout=httpx.Timeout(timeout),
        httpx_args=httpx_args,
    )
