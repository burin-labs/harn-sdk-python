from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

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

    def start(self) -> dict[str, Any]:
        response = self._http_client.post(
            f"{self._auth_base_url}/oauth/device/code",
            data={"client_id": self._client_id, "scope": self._scope},
        )
        response.raise_for_status()
        return response.json()

    def poll(
        self, device_code: str, interval: int = 5, timeout_seconds: int = 300
    ) -> str:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            response = self._http_client.post(
                f"{self._auth_base_url}/oauth/token",
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

            payload = response.json()
            if payload.get("error") in {"authorization_pending", "slow_down"}:
                time.sleep(interval)
                continue
            response.raise_for_status()
        raise TimeoutError("Timed out waiting for OAuth device authorization")

    def get_token(self) -> str | None:
        return self._token
