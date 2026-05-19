from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from .auth import AmbientCredential, CredentialProvider
from .models import ApiError, ErrorBody, JsonDict
from .stream import SSEParser, parse_sse_lines

HARN_PROTOCOL_VERSION = "agents-protocol-2026-04-25"
HARN_PROTOCOL_HEADER = "Harn-Agents-Protocol-Version"


def _path_segment(value: str) -> str:
    return quote(value, safe="")


def _parse_response(response: httpx.Response) -> Any:
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

    if response.status_code == 204:
        return None
    if response.headers.get("content-type", "").startswith("application/json"):
        return response.json()
    return response.content


class _BaseClient:
    def __init__(
        self,
        base_url: str = "https://api.harnlang.com",
        token: str | None = None,
        credential: CredentialProvider | None = None,
        timeout: float = 30.0,
        protocol_version: str = HARN_PROTOCOL_VERSION,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.protocol_version = protocol_version
        self.credential = credential
        self.token = token

    def _auth_headers(self, *, protocol: bool = True) -> dict[str, str]:
        token = self.token
        if token is None and self.credential is not None:
            token = self.credential.get_token()
        if token is None:
            token = AmbientCredential().get_token()
        headers = {}
        if protocol:
            headers[HARN_PROTOCOL_HEADER] = self.protocol_version
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
        protocol_version: str = HARN_PROTOCOL_VERSION,
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
        protocol: bool = True,
    ) -> Any:
        headers = self._auth_headers(protocol=protocol)
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        response = self._client.request(
            method, path, params=params, json=json, headers=headers
        )
        return _parse_response(response)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
        protocol: bool = True,
    ) -> Any:
        return self._request(
            method,
            path,
            params=params,
            json=body,
            idempotency_key=idempotency_key,
            protocol=protocol,
        )

    def _stream(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        protocol: bool = True,
    ):
        headers = self._auth_headers(protocol=protocol)
        with self._client.stream(
            "GET", path, params=params, headers=headers
        ) as response:
            response.raise_for_status()
            yield from parse_sse_lines(response.iter_lines())

    def get_protocol_discovery(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1", params=params, protocol=False)

    def get_agent_card(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/agent-card", params=params, protocol=False)

    def get_well_known_agent_card(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request(
            "GET", "/.well-known/agent-card.json", params=params, protocol=False
        )

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
        return self._request(
            "GET", f"/v1/personas/{_path_segment(persona_id)}", params=params
        )

    def get_persona_card(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/personas/{_path_segment(persona_id)}/card", params=params
        )

    def get_persona_manifest(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET",
            f"/v1/personas/{_path_segment(persona_id)}/manifest",
            params=params,
        )

    def get_persona_schedule_state(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET",
            f"/v1/personas/{_path_segment(persona_id)}/schedule/state",
            params=params,
        )

    def pause_persona_schedule(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/personas/{_path_segment(persona_id)}/schedule/pause",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def resume_persona_schedule(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/personas/{_path_segment(persona_id)}/schedule/resume",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def update_persona(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "PATCH",
            f"/v1/personas/{_path_segment(persona_id)}",
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
        return self._request(
            "GET", f"/v1/workspaces/{_path_segment(workspace_id)}", params=params
        )

    def update_workspace(
        self,
        workspace_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "PATCH",
            f"/v1/workspaces/{_path_segment(workspace_id)}",
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
        return self._request(
            "GET", f"/v1/sessions/{_path_segment(session_id)}", params=params
        )

    def update_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "PATCH",
            f"/v1/sessions/{_path_segment(session_id)}",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def suspend_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/sessions/{_path_segment(session_id)}/suspend",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def resume_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/sessions/{_path_segment(session_id)}/resume",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_session_audit(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/sessions/{_path_segment(session_id)}/audit", params=params
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
            f"/v1/sessions/{_path_segment(session_id)}/close",
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
            f"/v1/sessions/{_path_segment(session_id)}/fork",
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
            "GET", f"/v1/sessions/{_path_segment(session_id)}/messages", params=params
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
            f"/v1/sessions/{_path_segment(session_id)}/messages",
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
        return self._request(
            "GET", f"/v1/sessions/{_path_segment(session_id)}/tasks", params=params
        )

    def submit_session_task(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/sessions/{_path_segment(session_id)}/tasks",
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
            "GET", f"/v1/sessions/{_path_segment(session_id)}/branches", params=params
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
            f"/v1/sessions/{_path_segment(session_id)}/branches",
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
        return self._request(
            "GET", f"/v1/sessions/{_path_segment(session_id)}/events", params=params
        )

    def stream_session_events(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._stream(
            f"/v1/sessions/{_path_segment(session_id)}/events/stream", params=params
        )

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
        return self._request(
            "GET", f"/v1/tasks/{_path_segment(task_id)}", params=params
        )

    def cancel_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/tasks/{_path_segment(task_id)}/cancel",
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
            f"/v1/tasks/{_path_segment(task_id)}/replay",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def suspend_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/tasks/{_path_segment(task_id)}/suspend",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def resume_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/tasks/{_path_segment(task_id)}/resume",
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
            f"/v1/tasks/{_path_segment(task_id)}/messages",
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
        return self._request(
            "GET", f"/v1/tasks/{_path_segment(task_id)}/events", params=params
        )

    def stream_task_events(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._stream(f"/v1/tasks/{_path_segment(task_id)}/stream", params=params)

    def list_task_receipts(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/tasks/{_path_segment(task_id)}/receipts", params=params
        )

    def get_branch(
        self,
        branch_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/branches/{_path_segment(branch_id)}", params=params
        )

    def get_message(
        self,
        message_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/messages/{_path_segment(message_id)}", params=params
        )

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
        return self._request(
            "GET", f"/v1/artifacts/{_path_segment(artifact_id)}", params=params
        )

    def download_artifact_content(
        self,
        artifact_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/artifacts/{_path_segment(artifact_id)}/content", params=params
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
        return self._request(
            "GET", f"/v1/events/{_path_segment(event_id)}", params=params
        )

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
        return self._request(
            "GET", f"/v1/receipts/{_path_segment(receipt_id)}", params=params
        )

    def verify_receipt(
        self,
        receipt_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/receipts/{_path_segment(receipt_id)}/verify",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_lifecycle_audit(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/audit/lifecycle", params=params)

    def list_pipeline_audit(
        self,
        pipeline_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/pipelines/{_path_segment(pipeline_id)}/audit", params=params
        )

    def list_channel_events(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/channel-events", params=params)

    def list_context_packs(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/context-packs", params=params)

    def create_context_pack(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/context-packs",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def get_context_pack(
        self,
        pack_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/context-packs/{_path_segment(pack_id)}", params=params
        )

    def diff_context_pack(
        self,
        pack_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET", f"/v1/context-packs/{_path_segment(pack_id)}/diff", params=params
        )

    def get_context_pack_version(
        self,
        pack_id: str,
        version: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET",
            f"/v1/context-packs/{_path_segment(pack_id)}/versions/{_path_segment(version)}",
            params=params,
        )

    def approve_context_pack_version(
        self,
        pack_id: str,
        version: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/context-packs/{_path_segment(pack_id)}/versions/{_path_segment(version)}/approve",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def revoke_context_pack_version(
        self,
        pack_id: str,
        version: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/context-packs/{_path_segment(pack_id)}/versions/{_path_segment(version)}/revoke",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def review_context_pack_artifact(
        self,
        pack_id: str,
        version: str,
        artifact_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            f"/v1/context-packs/{_path_segment(pack_id)}/versions/{_path_segment(version)}/artifacts/{_path_segment(artifact_id)}/review",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def resolve_context_pack_mounts(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/context-packs/mounts/resolve",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_tool_call_receipts(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return self._request("GET", "/v1/tool-call-receipts", params=params)

    def search_tool_call_receipts(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "POST",
            "/v1/tool-call-receipts/search",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    def list_run_tool_call_receipts(
        self,
        run_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "GET",
            f"/v1/runs/{_path_segment(run_id)}/tool-call-receipts",
            params=params,
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
        return self._request(
            "GET", f"/v1/memories/{_path_segment(memory_id)}", params=params
        )

    def delete_memory(
        self,
        memory_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self._request(
            "DELETE", f"/v1/memories/{_path_segment(memory_id)}", params=params
        )

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
        return self._request(
            "GET", f"/v1/vaults/{_path_segment(vault_id)}", params=params
        )

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
        return self._request(
            "GET", f"/v1/connectors/{_path_segment(connector_id)}", params=params
        )

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
        return self._request(
            "GET", f"/v1/skills/{_path_segment(skill_id)}", params=params
        )

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
        return self._request(
            "GET", f"/v1/outcomes/{_path_segment(outcome_id)}", params=params
        )

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
        return self._request(
            "GET", f"/v1/quotas/{_path_segment(quota_id)}", params=params
        )


class AsyncHarnClient(_BaseClient):
    def __init__(
        self,
        base_url: str = "https://api.harnlang.com",
        token: str | None = None,
        credential: CredentialProvider | None = None,
        timeout: float = 30.0,
        protocol_version: str = HARN_PROTOCOL_VERSION,
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
        protocol: bool = True,
    ) -> Any:
        headers = self._auth_headers(protocol=protocol)
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        response = await self._client.request(
            method, path, params=params, json=json, headers=headers
        )
        return _parse_response(response)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
        protocol: bool = True,
    ) -> Any:
        return await self._request(
            method,
            path,
            params=params,
            json=body,
            idempotency_key=idempotency_key,
            protocol=protocol,
        )

    async def _stream(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        protocol: bool = True,
    ):
        headers = self._auth_headers(protocol=protocol)
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
        return await self._request("GET", "/v1", params=params, protocol=False)

    async def get_agent_card(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request(
            "GET", "/v1/agent-card", params=params, protocol=False
        )

    async def get_well_known_agent_card(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request(
            "GET", "/.well-known/agent-card.json", params=params, protocol=False
        )

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
        return await self._request(
            "GET", f"/v1/personas/{_path_segment(persona_id)}", params=params
        )

    async def get_persona_card(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/personas/{_path_segment(persona_id)}/card", params=params
        )

    async def get_persona_manifest(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET",
            f"/v1/personas/{_path_segment(persona_id)}/manifest",
            params=params,
        )

    async def get_persona_schedule_state(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET",
            f"/v1/personas/{_path_segment(persona_id)}/schedule/state",
            params=params,
        )

    async def pause_persona_schedule(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/personas/{_path_segment(persona_id)}/schedule/pause",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def resume_persona_schedule(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/personas/{_path_segment(persona_id)}/schedule/resume",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def update_persona(
        self,
        persona_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "PATCH",
            f"/v1/personas/{_path_segment(persona_id)}",
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
            "GET", f"/v1/workspaces/{_path_segment(workspace_id)}", params=params
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
            f"/v1/workspaces/{_path_segment(workspace_id)}",
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
        return await self._request(
            "GET", f"/v1/sessions/{_path_segment(session_id)}", params=params
        )

    async def update_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "PATCH",
            f"/v1/sessions/{_path_segment(session_id)}",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def suspend_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/sessions/{_path_segment(session_id)}/suspend",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def resume_session(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/sessions/{_path_segment(session_id)}/resume",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_session_audit(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/sessions/{_path_segment(session_id)}/audit", params=params
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
            f"/v1/sessions/{_path_segment(session_id)}/close",
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
            f"/v1/sessions/{_path_segment(session_id)}/fork",
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
            "GET", f"/v1/sessions/{_path_segment(session_id)}/messages", params=params
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
            f"/v1/sessions/{_path_segment(session_id)}/messages",
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
            "GET", f"/v1/sessions/{_path_segment(session_id)}/tasks", params=params
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
            f"/v1/sessions/{_path_segment(session_id)}/tasks",
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
            "GET", f"/v1/sessions/{_path_segment(session_id)}/branches", params=params
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
            f"/v1/sessions/{_path_segment(session_id)}/branches",
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
            "GET", f"/v1/sessions/{_path_segment(session_id)}/events", params=params
        )

    async def stream_session_events(
        self,
        session_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        async for event in self._stream(
            f"/v1/sessions/{_path_segment(session_id)}/events/stream", params=params
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
        return await self._request(
            "GET", f"/v1/tasks/{_path_segment(task_id)}", params=params
        )

    async def cancel_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/tasks/{_path_segment(task_id)}/cancel",
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
            f"/v1/tasks/{_path_segment(task_id)}/replay",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def suspend_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/tasks/{_path_segment(task_id)}/suspend",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def resume_task(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/tasks/{_path_segment(task_id)}/resume",
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
            f"/v1/tasks/{_path_segment(task_id)}/messages",
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
        return await self._request(
            "GET", f"/v1/tasks/{_path_segment(task_id)}/events", params=params
        )

    async def stream_task_events(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        async for event in self._stream(
            f"/v1/tasks/{_path_segment(task_id)}/stream", params=params
        ):
            yield event

    async def list_task_receipts(
        self,
        task_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/tasks/{_path_segment(task_id)}/receipts", params=params
        )

    async def get_branch(
        self,
        branch_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/branches/{_path_segment(branch_id)}", params=params
        )

    async def get_message(
        self,
        message_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/messages/{_path_segment(message_id)}", params=params
        )

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
        return await self._request(
            "GET", f"/v1/artifacts/{_path_segment(artifact_id)}", params=params
        )

    async def download_artifact_content(
        self,
        artifact_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/artifacts/{_path_segment(artifact_id)}/content", params=params
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
        return await self._request(
            "GET", f"/v1/events/{_path_segment(event_id)}", params=params
        )

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
        return await self._request(
            "GET", f"/v1/receipts/{_path_segment(receipt_id)}", params=params
        )

    async def verify_receipt(
        self,
        receipt_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/receipts/{_path_segment(receipt_id)}/verify",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_lifecycle_audit(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/audit/lifecycle", params=params)

    async def list_pipeline_audit(
        self,
        pipeline_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/pipelines/{_path_segment(pipeline_id)}/audit", params=params
        )

    async def list_channel_events(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/channel-events", params=params)

    async def list_context_packs(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/context-packs", params=params)

    async def create_context_pack(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/context-packs",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def get_context_pack(
        self,
        pack_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/context-packs/{_path_segment(pack_id)}", params=params
        )

    async def diff_context_pack(
        self,
        pack_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET", f"/v1/context-packs/{_path_segment(pack_id)}/diff", params=params
        )

    async def get_context_pack_version(
        self,
        pack_id: str,
        version: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET",
            f"/v1/context-packs/{_path_segment(pack_id)}/versions/{_path_segment(version)}",
            params=params,
        )

    async def approve_context_pack_version(
        self,
        pack_id: str,
        version: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/context-packs/{_path_segment(pack_id)}/versions/{_path_segment(version)}/approve",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def revoke_context_pack_version(
        self,
        pack_id: str,
        version: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/context-packs/{_path_segment(pack_id)}/versions/{_path_segment(version)}/revoke",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def review_context_pack_artifact(
        self,
        pack_id: str,
        version: str,
        artifact_id: str,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            f"/v1/context-packs/{_path_segment(pack_id)}/versions/{_path_segment(version)}/artifacts/{_path_segment(artifact_id)}/review",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def resolve_context_pack_mounts(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/context-packs/mounts/resolve",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_tool_call_receipts(
        self, params: dict[str, Any] | None = None, idempotency_key: str | None = None
    ) -> Any:
        return await self._request("GET", "/v1/tool-call-receipts", params=params)

    async def search_tool_call_receipts(
        self,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "POST",
            "/v1/tool-call-receipts/search",
            params=params,
            json=body,
            idempotency_key=idempotency_key,
        )

    async def list_run_tool_call_receipts(
        self,
        run_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "GET",
            f"/v1/runs/{_path_segment(run_id)}/tool-call-receipts",
            params=params,
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
        return await self._request(
            "GET", f"/v1/memories/{_path_segment(memory_id)}", params=params
        )

    async def delete_memory(
        self,
        memory_id: str,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._request(
            "DELETE", f"/v1/memories/{_path_segment(memory_id)}", params=params
        )

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
        return await self._request(
            "GET", f"/v1/vaults/{_path_segment(vault_id)}", params=params
        )

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
            "GET", f"/v1/connectors/{_path_segment(connector_id)}", params=params
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
        return await self._request(
            "GET", f"/v1/skills/{_path_segment(skill_id)}", params=params
        )

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
        return await self._request(
            "GET", f"/v1/outcomes/{_path_segment(outcome_id)}", params=params
        )

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
        return await self._request(
            "GET", f"/v1/quotas/{_path_segment(quota_id)}", params=params
        )
