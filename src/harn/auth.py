from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import httpx


class CredentialProvider:
    def get_token(self) -> str | None:
        raise NotImplementedError


@dataclass
class APIKeyCredential(CredentialProvider):
    api_key: str

    def get_token(self) -> str:
        return self.api_key


@dataclass
class AmbientCredential(CredentialProvider):
    env_var: str = "HARN_API_KEY"

    def get_token(self) -> str | None:
        return os.getenv(self.env_var)


class OAuthDeviceFlowCredential(CredentialProvider):
    def __init__(
        self,
        auth_base_url: str,
        client_id: str,
        scope: str,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._auth_base_url = auth_base_url.rstrip("/")
        self._client_id = client_id
        self._scope = scope
        self._http_client = http_client or httpx.Client(timeout=30.0)
        self._token: str | None = None
        self._device_authorization_endpoint: str | None = None
        self._token_endpoint: str | None = None

    def discover(self) -> dict[str, Any]:
        response = self._http_client.get(
            urljoin(f"{self._auth_base_url}/", ".well-known/openid-configuration")
        )
        response.raise_for_status()
        payload = response.json()
        self._device_authorization_endpoint = payload.get(
            "device_authorization_endpoint"
        )
        self._token_endpoint = payload.get("token_endpoint")
        if not self._device_authorization_endpoint or not self._token_endpoint:
            raise ValueError(
                "OIDC discovery document does not advertise device authorization and token endpoints"
            )
        return payload

    def start(self) -> dict[str, Any]:
        endpoint = self._device_authorization_endpoint
        if endpoint is None:
            endpoint = f"{self._auth_base_url}/oauth/device/code"
        response = self._http_client.post(
            endpoint,
            data={"client_id": self._client_id, "scope": self._scope},
        )
        response.raise_for_status()
        authorization = response.json()
        if self._token_endpoint is not None:
            authorization["token_endpoint"] = self._token_endpoint
        return authorization

    def poll(
        self, device_code: str, interval: int = 5, timeout_seconds: int = 300
    ) -> str:
        deadline = time.monotonic() + timeout_seconds
        token_endpoint = self._token_endpoint or f"{self._auth_base_url}/oauth/token"
        while time.monotonic() < deadline:
            response = self._http_client.post(
                token_endpoint,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": device_code,
                    "client_id": self._client_id,
                },
            )
            if response.status_code == 200:
                token = response.json()["access_token"]
                self._token = token
                return token

            payload = _safe_json(response)
            error = payload.get("error")
            if error == "slow_down":
                interval += 5
                time.sleep(interval)
                continue
            if error == "authorization_pending":
                time.sleep(interval)
                continue
            response.raise_for_status()
        raise TimeoutError("Timed out waiting for OAuth device authorization")

    def get_token(self) -> str | None:
        return self._token


def _safe_json(response: httpx.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        return {}
    return payload if isinstance(payload, dict) else {}
