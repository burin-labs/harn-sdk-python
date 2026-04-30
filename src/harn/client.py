from __future__ import annotations

from typing import Any

import httpx

from .auth import AmbientCredential, CredentialProvider
from .models import ApiError, ErrorBody, JsonDict
from .stream import SSEParser, parse_sse_lines


class _BaseClient:
    def __init__(
        self,
        base_url: str = "https://api.harnlang.com",
        token: str | None = None,
        credential: CredentialProvider | None = None,
        timeout: float = 30.0,
        protocol_version: str = "v1",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.protocol_version = protocol_version
        self.credential = credential
        self.token = token

    def _auth_headers(self) -> dict[str, str]:
        token = self.token
        if token is None and self.credential is not None:
            token = self.credential.get_token()
        if token is None:
            token = AmbientCredential().get_token()
        headers = {"X-Harn-Protocol-Version": self.protocol_version}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers


class HarnClient(_BaseClient):
    def __init__(
        self,
        base_url: str = "https://api.harnlang.com",
        token: str | None = None,
        credential: CredentialProvider | None = None,
        timeout: float = 30.0,
        protocol_version: str = "v1",
        client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            token=token,
            credential=credential,
            timeout=timeout,
            protocol_version=protocol_version,
        )
        self._client = client or httpx.Client(
            base_url=self.base_url, timeout=self.timeout
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "HarnClient":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        headers = self._auth_headers()
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        response = self._client.request(
            method, path, params=params, json=json, headers=headers
        )
        if response.is_error:
            error = None
            body: Any
            try:
                body = response.json()
                if (
                    isinstance(body, dict)
                    and "error" in body
                    and isinstance(body["error"], dict)
                ):
                    error = ErrorBody.model_validate(body["error"])
            except Exception:
                body = response.text
            raise ApiError(response.status_code, error, body)

        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return response.content

    def _stream(self, path: str, *, params: dict[str, Any] | None = None):
        headers = self._auth_headers()
        with self._client.stream(
            "GET", path, params=params, headers=headers
        ) as response:
            response.raise_for_status()
            yield from parse_sse_lines(response.iter_lines())

    def get_protocol_discovery(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1", params=params)

    def get_agent_card(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/agent-card", params=params)

    def list_personas(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/personas", params=params)

    def create_persona(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/personas",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def get_persona(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/personas/{persona_id}", params=params)

    def update_persona(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "PATCH",
            f"/v1/personas/{persona_id}",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_workspaces(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/workspaces", params=params)

    def create_workspace(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/workspaces",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def get_workspace(
        self,
        workspace_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/workspaces/{workspace_id}", params=params)

    def update_workspace(
        self,
        workspace_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "PATCH",
            f"/v1/workspaces/{workspace_id}",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_sessions(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/sessions", params=params)

    def create_session(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/sessions",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def get_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/sessions/{session_id}", params=params)

    def update_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "PATCH",
            f"/v1/sessions/{session_id}",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def close_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/sessions/{session_id}/close",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def fork_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/sessions/{session_id}/fork",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_session_messages(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/sessions/{session_id}/messages", params=params
        )

    def append_session_message(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/sessions/{session_id}/messages",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_session_tasks(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/sessions/{session_id}/tasks", params=params)

    def submit_session_task(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/sessions/{session_id}/tasks",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_session_branches(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/sessions/{session_id}/branches", params=params
        )

    def create_session_branch(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/sessions/{session_id}/branches",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_session_events(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/sessions/{session_id}/events", params=params)

    def stream_session_events(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._stream(f"/v1/sessions/{session_id}/events/stream", params=params)

    def list_tasks(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/tasks", params=params)

    def submit_task(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/tasks",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def get_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/tasks/{task_id}", params=params)

    def cancel_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/tasks/{task_id}/cancel",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def replay_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/tasks/{task_id}/replay",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def append_task_message(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/tasks/{task_id}/messages",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_task_events(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/tasks/{task_id}/events", params=params)

    def stream_task_events(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._stream(f"/v1/tasks/{task_id}/stream", params=params)

    def list_task_receipts(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/tasks/{task_id}/receipts", params=params)

    def get_branch(
        self,
        branch_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/branches/{branch_id}", params=params)

    def get_message(
        self,
        message_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/messages/{message_id}", params=params)

    def list_artifacts(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/artifacts", params=params)

    def register_artifact(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/artifacts",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def get_artifact(
        self,
        artifact_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/artifacts/{artifact_id}", params=params)

    def download_artifact_content(
        self,
        artifact_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/artifacts/{artifact_id}/content", params=params
        )

    def list_events(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/events", params=params)

    def get_event(
        self,
        event_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/events/{event_id}", params=params)

    def stream_events(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._stream("/v1/events/stream", params=params)

    def get_receipt(
        self,
        receipt_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/receipts/{receipt_id}", params=params)

    def verify_receipt(
        self,
        receipt_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/receipts/{receipt_id}/verify",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_memories(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/memories", params=params)

    def create_memory(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/memories",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def get_memory(
        self,
        memory_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/memories/{memory_id}", params=params)

    def delete_memory(
        self,
        memory_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("DELETE", f"/v1/memories/{memory_id}", params=params)

    def list_vaults(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/vaults", params=params)

    def create_vault(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/vaults",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def get_vault(
        self,
        vault_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/vaults/{vault_id}", params=params)

    def list_connectors(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/connectors", params=params)

    def get_connector(
        self,
        connector_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/connectors/{connector_id}", params=params)

    def list_skills(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/skills", params=params)

    def get_skill(
        self,
        skill_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/skills/{skill_id}", params=params)

    def list_outcomes(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/outcomes", params=params)

    def get_outcome(
        self,
        outcome_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/outcomes/{outcome_id}", params=params)

    def list_quotas(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/quotas", params=params)

    def get_quota(
        self,
        quota_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request("GET", f"/v1/quotas/{quota_id}", params=params)


class AsyncHarnClient(_BaseClient):
    def __init__(
        self,
        base_url: str = "https://api.harnlang.com",
        token: str | None = None,
        credential: CredentialProvider | None = None,
        timeout: float = 30.0,
        protocol_version: str = "v1",
        client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            token=token,
            credential=credential,
            timeout=timeout,
            protocol_version=protocol_version,
        )
        self._client = client or httpx.AsyncClient(
            base_url=self.base_url, timeout=self.timeout
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncHarnClient":
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        headers = self._auth_headers()
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        response = await self._client.request(
            method, path, params=params, json=json, headers=headers
        )
        if response.is_error:
            error = None
            body: Any
            try:
                body = response.json()
                if (
                    isinstance(body, dict)
                    and "error" in body
                    and isinstance(body["error"], dict)
                ):
                    error = ErrorBody.model_validate(body["error"])
            except Exception:
                body = response.text
            raise ApiError(response.status_code, error, body)

        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return response.content

    async def _stream(self, path: str, *, params: dict[str, Any] | None = None):
        headers = self._auth_headers()
        parser = SSEParser()
        async with self._client.stream(
            "GET", path, params=params, headers=headers
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                event = parser.push(line)
                if event is not None:
                    yield event
        tail = parser.finish()
        if tail is not None:
            yield tail

    async def get_protocol_discovery(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1", params=params)

    async def get_agent_card(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/agent-card", params=params)

    async def list_personas(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/personas", params=params)

    async def create_persona(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/personas",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def get_persona(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/personas/{persona_id}", params=params)

    async def update_persona(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "PATCH",
            f"/v1/personas/{persona_id}",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_workspaces(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/workspaces", params=params)

    async def create_workspace(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/workspaces",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def get_workspace(
        self,
        workspace_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/workspaces/{workspace_id}", params=params
        )

    async def update_workspace(
        self,
        workspace_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "PATCH",
            f"/v1/workspaces/{workspace_id}",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_sessions(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/sessions", params=params)

    async def create_session(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/sessions",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def get_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/sessions/{session_id}", params=params)

    async def update_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "PATCH",
            f"/v1/sessions/{session_id}",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def close_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/sessions/{session_id}/close",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def fork_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/sessions/{session_id}/fork",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_session_messages(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/sessions/{session_id}/messages", params=params
        )

    async def append_session_message(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/sessions/{session_id}/messages",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_session_tasks(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/sessions/{session_id}/tasks", params=params
        )

    async def submit_session_task(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/sessions/{session_id}/tasks",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_session_branches(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/sessions/{session_id}/branches", params=params
        )

    async def create_session_branch(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/sessions/{session_id}/branches",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_session_events(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/sessions/{session_id}/events", params=params
        )

    async def stream_session_events(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        async for event in self._stream(
            f"/v1/sessions/{session_id}/events/stream", params=params
        ):
            yield event

    async def list_tasks(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/tasks", params=params)

    async def submit_task(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/tasks",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def get_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/tasks/{task_id}", params=params)

    async def cancel_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/tasks/{task_id}/cancel",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def replay_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/tasks/{task_id}/replay",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def append_task_message(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/tasks/{task_id}/messages",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_task_events(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/tasks/{task_id}/events", params=params)

    async def stream_task_events(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        async for event in self._stream(f"/v1/tasks/{task_id}/stream", params=params):
            yield event

    async def list_task_receipts(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/tasks/{task_id}/receipts", params=params
        )

    async def get_branch(
        self,
        branch_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/branches/{branch_id}", params=params)

    async def get_message(
        self,
        message_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/messages/{message_id}", params=params)

    async def list_artifacts(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/artifacts", params=params)

    async def register_artifact(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/artifacts",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def get_artifact(
        self,
        artifact_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/artifacts/{artifact_id}", params=params)

    async def download_artifact_content(
        self,
        artifact_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/artifacts/{artifact_id}/content", params=params
        )

    async def list_events(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/events", params=params)

    async def get_event(
        self,
        event_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/events/{event_id}", params=params)

    async def stream_events(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        async for event in self._stream("/v1/events/stream", params=params):
            yield event

    async def get_receipt(
        self,
        receipt_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/receipts/{receipt_id}", params=params)

    async def verify_receipt(
        self,
        receipt_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/receipts/{receipt_id}/verify",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_memories(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/memories", params=params)

    async def create_memory(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/memories",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def get_memory(
        self,
        memory_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/memories/{memory_id}", params=params)

    async def delete_memory(
        self,
        memory_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("DELETE", f"/v1/memories/{memory_id}", params=params)

    async def list_vaults(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/vaults", params=params)

    async def create_vault(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/vaults",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def get_vault(
        self,
        vault_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/vaults/{vault_id}", params=params)

    async def list_connectors(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/connectors", params=params)

    async def get_connector(
        self,
        connector_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/connectors/{connector_id}", params=params
        )

    async def list_skills(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/skills", params=params)

    async def get_skill(
        self,
        skill_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/skills/{skill_id}", params=params)

    async def list_outcomes(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/outcomes", params=params)

    async def get_outcome(
        self,
        outcome_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/outcomes/{outcome_id}", params=params)

    async def list_quotas(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/quotas", params=params)

    async def get_quota(
        self,
        quota_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request("GET", f"/v1/quotas/{quota_id}", params=params)
