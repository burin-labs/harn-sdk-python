from __future__ import annotations

import re
from collections.abc import AsyncIterator, Iterator
from dataclasses import dataclass
from inspect import Parameter, Signature
from typing import Any
from urllib.parse import quote

import httpx

from .auth import AmbientCredential, CredentialProvider
from .models import ApiError, ErrorBody, JsonDict, StreamEvent
from .stream import SSEParser, parse_sse_lines

HARN_PROTOCOL_VERSION = "agents-protocol-2026-04-25"
HARN_PROTOCOL_HEADER = "Harn-Agents-Protocol-Version"

_PATH_PARAM_RE = re.compile(r"{([A-Za-z_][A-Za-z0-9_]*)}")


@dataclass(frozen=True)
class _Endpoint:
    name: str
    method: str
    path: str
    public: bool = False
    stream: bool = False
    accepts_body: bool = False

    @property
    def path_params(self) -> tuple[str, ...]:
        return tuple(_PATH_PARAM_RE.findall(self.path))


_OPENAPI_ENDPOINTS: tuple[_Endpoint, ...] = (
    _Endpoint("get_health", "GET", "/health", public=True),
    _Endpoint("get_version", "GET", "/version", public=True),
    _Endpoint("get_open_api_document", "GET", "/openapi.json", public=True),
    _Endpoint("get_protocol_discovery", "GET", "/v1", public=True),
    _Endpoint("get_runtime", "GET", "/v1/runtime"),
    _Endpoint("list_capabilities", "GET", "/v1/capabilities"),
    _Endpoint("list_tools", "GET", "/v1/tools"),
    _Endpoint("get_tool", "GET", "/v1/tools/{tool_id}"),
    _Endpoint("get_agent_card", "GET", "/v1/agent-card", public=True),
    _Endpoint("list_personas", "GET", "/v1/personas"),
    _Endpoint("create_persona", "POST", "/v1/personas", accepts_body=True),
    _Endpoint("get_persona", "GET", "/v1/personas/{persona_id}"),
    _Endpoint(
        "update_persona",
        "PATCH",
        "/v1/personas/{persona_id}",
        accepts_body=True,
    ),
    _Endpoint("list_workspaces", "GET", "/v1/workspaces"),
    _Endpoint("create_workspace", "POST", "/v1/workspaces", accepts_body=True),
    _Endpoint("get_workspace", "GET", "/v1/workspaces/{workspace_id}"),
    _Endpoint(
        "update_workspace",
        "PATCH",
        "/v1/workspaces/{workspace_id}",
        accepts_body=True,
    ),
    _Endpoint("read_workspace_file", "GET", "/v1/workspaces/{workspace_id}/files"),
    _Endpoint(
        "write_workspace_file",
        "PUT",
        "/v1/workspaces/{workspace_id}/files",
        accepts_body=True,
    ),
    _Endpoint("list_sessions", "GET", "/v1/sessions"),
    _Endpoint("create_session", "POST", "/v1/sessions", accepts_body=True),
    _Endpoint("get_session", "GET", "/v1/sessions/{session_id}"),
    _Endpoint(
        "update_session",
        "PATCH",
        "/v1/sessions/{session_id}",
        accepts_body=True,
    ),
    _Endpoint("close_session", "POST", "/v1/sessions/{session_id}/close"),
    _Endpoint(
        "fork_session",
        "POST",
        "/v1/sessions/{session_id}/fork",
        accepts_body=True,
    ),
    _Endpoint(
        "truncate_session",
        "POST",
        "/v1/sessions/{session_id}/truncate",
        accepts_body=True,
    ),
    _Endpoint("list_session_messages", "GET", "/v1/sessions/{session_id}/messages"),
    _Endpoint(
        "append_session_message",
        "POST",
        "/v1/sessions/{session_id}/messages",
        accepts_body=True,
    ),
    _Endpoint("list_session_tasks", "GET", "/v1/sessions/{session_id}/tasks"),
    _Endpoint(
        "submit_session_task",
        "POST",
        "/v1/sessions/{session_id}/tasks",
        accepts_body=True,
    ),
    _Endpoint("list_session_branches", "GET", "/v1/sessions/{session_id}/branches"),
    _Endpoint(
        "create_session_branch",
        "POST",
        "/v1/sessions/{session_id}/branches",
        accepts_body=True,
    ),
    _Endpoint("list_session_events", "GET", "/v1/sessions/{session_id}/events"),
    _Endpoint(
        "stream_session_events",
        "GET",
        "/v1/sessions/{session_id}/events/stream",
        stream=True,
    ),
    _Endpoint("list_tasks", "GET", "/v1/tasks"),
    _Endpoint("submit_task", "POST", "/v1/tasks", accepts_body=True),
    _Endpoint("get_task", "GET", "/v1/tasks/{task_id}"),
    _Endpoint(
        "cancel_task",
        "POST",
        "/v1/tasks/{task_id}/cancel",
        accepts_body=True,
    ),
    _Endpoint("list_permission_requests", "GET", "/v1/permission-requests"),
    _Endpoint(
        "list_task_permission_requests",
        "GET",
        "/v1/tasks/{task_id}/permission-requests",
    ),
    _Endpoint(
        "respond_permission_request",
        "POST",
        "/v1/permission-requests/{request_id}/respond",
        accepts_body=True,
    ),
    _Endpoint(
        "replay_task",
        "POST",
        "/v1/tasks/{task_id}/replay",
        accepts_body=True,
    ),
    _Endpoint(
        "append_task_message",
        "POST",
        "/v1/tasks/{task_id}/messages",
        accepts_body=True,
    ),
    _Endpoint("list_task_events", "GET", "/v1/tasks/{task_id}/events"),
    _Endpoint("stream_task_events", "GET", "/v1/tasks/{task_id}/stream", stream=True),
    _Endpoint("list_task_receipts", "GET", "/v1/tasks/{task_id}/receipts"),
    _Endpoint("get_branch", "GET", "/v1/branches/{branch_id}"),
    _Endpoint("get_message", "GET", "/v1/messages/{message_id}"),
    _Endpoint("list_artifacts", "GET", "/v1/artifacts"),
    _Endpoint("register_artifact", "POST", "/v1/artifacts", accepts_body=True),
    _Endpoint("get_artifact", "GET", "/v1/artifacts/{artifact_id}"),
    _Endpoint(
        "download_artifact_content",
        "GET",
        "/v1/artifacts/{artifact_id}/content",
    ),
    _Endpoint("list_events", "GET", "/v1/events"),
    _Endpoint("get_event", "GET", "/v1/events/{event_id}"),
    _Endpoint("stream_events", "GET", "/v1/events/stream", stream=True),
    _Endpoint("get_receipt", "GET", "/v1/receipts/{receipt_id}"),
    _Endpoint(
        "verify_receipt",
        "POST",
        "/v1/receipts/{receipt_id}/verify",
        accepts_body=True,
    ),
    _Endpoint("list_memories", "GET", "/v1/memories"),
    _Endpoint("create_memory", "POST", "/v1/memories", accepts_body=True),
    _Endpoint("get_memory", "GET", "/v1/memories/{memory_id}"),
    _Endpoint("delete_memory", "DELETE", "/v1/memories/{memory_id}"),
    _Endpoint("list_vaults", "GET", "/v1/vaults"),
    _Endpoint("create_vault", "POST", "/v1/vaults", accepts_body=True),
    _Endpoint("get_vault", "GET", "/v1/vaults/{vault_id}"),
    _Endpoint("list_connectors", "GET", "/v1/connectors"),
    _Endpoint("get_connector", "GET", "/v1/connectors/{connector_id}"),
    _Endpoint("list_skills", "GET", "/v1/skills"),
    _Endpoint("get_skill", "GET", "/v1/skills/{skill_id}"),
    _Endpoint("list_outcomes", "GET", "/v1/outcomes"),
    _Endpoint("get_outcome", "GET", "/v1/outcomes/{outcome_id}"),
    _Endpoint("list_quotas", "GET", "/v1/quotas"),
    _Endpoint("get_quota", "GET", "/v1/quotas/{quota_id}"),
)


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
    if response.headers.get("content-type", "").lower().startswith("application/json"):
        return response.json()
    return response.content


def _render_endpoint_path(
    endpoint: _Endpoint,
    path_args: tuple[object, ...],
    path_kwargs: dict[str, object],
) -> str:
    names = endpoint.path_params
    if len(path_args) > len(names):
        raise TypeError(
            f"{endpoint.name}() takes {len(names)} path argument(s) "
            f"but {len(path_args)} were given"
        )

    values: dict[str, object] = {}
    for name, value in zip(names, path_args, strict=False):
        values[name] = value

    duplicate_names = set(values) & set(path_kwargs)
    if duplicate_names:
        duplicate = sorted(duplicate_names)[0]
        raise TypeError(f"{endpoint.name}() got multiple values for '{duplicate}'")

    missing = []
    for name in names[len(path_args) :]:
        try:
            values[name] = path_kwargs.pop(name)
        except KeyError:
            missing.append(name)
    if missing:
        missing_args = ", ".join(missing)
        raise TypeError(f"{endpoint.name}() missing path argument(s): {missing_args}")

    if path_kwargs:
        unexpected = ", ".join(sorted(path_kwargs))
        raise TypeError(
            f"{endpoint.name}() got unexpected path argument(s): {unexpected}"
        )

    path = endpoint.path
    for name, value in values.items():
        path = path.replace(f"{{{name}}}", _path_segment(str(value)))
    return path


def _prepare_endpoint_call(
    endpoint: _Endpoint,
    path_args: tuple[object, ...],
    path_kwargs: dict[str, object],
    body: JsonDict | None,
) -> tuple[str, bool, bool]:
    if body is not None and not endpoint.accepts_body:
        raise TypeError(f"{endpoint.name}() does not accept a body")
    path = _render_endpoint_path(endpoint, path_args, path_kwargs)
    auth = not endpoint.public
    protocol = not endpoint.public
    return path, auth, protocol


def _endpoint_signature(endpoint: _Endpoint) -> Signature:
    parameters = [
        Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
        for name in endpoint.path_params
    ]
    parameters.append(
        Parameter(
            "params",
            Parameter.KEYWORD_ONLY,
            default=None,
            annotation=dict[str, Any] | None,
        )
    )
    if endpoint.accepts_body:
        parameters.append(
            Parameter(
                "body",
                Parameter.KEYWORD_ONLY,
                default=None,
                annotation=JsonDict | None,
            )
        )
    parameters.append(
        Parameter(
            "idempotency_key",
            Parameter.KEYWORD_ONLY,
            default=None,
            annotation=str | None,
        )
    )
    return_annotation: object
    if endpoint.stream:
        return_annotation = Iterator[StreamEvent]
    else:
        return_annotation = Any
    return Signature(parameters, return_annotation=return_annotation)


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

    def _auth_headers(
        self, *, auth: bool = True, protocol: bool = True
    ) -> dict[str, str]:
        headers = {}
        if protocol:
            headers[HARN_PROTOCOL_HEADER] = self.protocol_version
        if not auth:
            return headers

        token = self.token
        if token is None and self.credential is not None:
            token = self.credential.get_token()
        if token is None:
            token = AmbientCredential().get_token()
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

    def __enter__(self) -> HarnClient:
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
        auth: bool = True,
        protocol: bool = True,
    ) -> Any:
        headers = self._auth_headers(auth=auth, protocol=protocol)
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
        auth: bool = True,
        protocol: bool = True,
    ) -> Any:
        return self._request(
            method,
            path,
            params=params,
            json=body,
            idempotency_key=idempotency_key,
            auth=auth,
            protocol=protocol,
        )

    def _stream(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        auth: bool = True,
        protocol: bool = True,
    ) -> Iterator[StreamEvent]:
        headers = self._auth_headers(auth=auth, protocol=protocol)
        with self._client.stream(
            "GET", path, params=params, headers=headers
        ) as response:
            if response.is_error:
                response.read()
                _parse_response(response)
            yield from parse_sse_lines(response.iter_lines())

    def _call_endpoint(
        self,
        endpoint: _Endpoint,
        path_args: tuple[object, ...],
        path_kwargs: dict[str, object],
        *,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        path, auth, protocol = _prepare_endpoint_call(
            endpoint, path_args, path_kwargs, body
        )
        if endpoint.stream:
            return self._stream(path, params=params, auth=auth, protocol=protocol)
        return self._request(
            endpoint.method,
            path,
            params=params,
            json=body,
            idempotency_key=idempotency_key,
            auth=auth,
            protocol=protocol,
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

    async def __aenter__(self) -> AsyncHarnClient:
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
        auth: bool = True,
        protocol: bool = True,
    ) -> Any:
        headers = self._auth_headers(auth=auth, protocol=protocol)
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
        auth: bool = True,
        protocol: bool = True,
    ) -> Any:
        return await self._request(
            method,
            path,
            params=params,
            json=body,
            idempotency_key=idempotency_key,
            auth=auth,
            protocol=protocol,
        )

    async def _stream(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        auth: bool = True,
        protocol: bool = True,
    ) -> AsyncIterator[StreamEvent]:
        headers = self._auth_headers(auth=auth, protocol=protocol)
        parser = SSEParser()
        async with self._client.stream(
            "GET", path, params=params, headers=headers
        ) as response:
            if response.is_error:
                await response.aread()
                _parse_response(response)
            async for line in response.aiter_lines():
                event = parser.push(line)
                if event is not None:
                    yield event
        tail = parser.finish()
        if tail is not None:
            yield tail

    async def _call_endpoint(
        self,
        endpoint: _Endpoint,
        path_args: tuple[object, ...],
        path_kwargs: dict[str, object],
        *,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        path, auth, protocol = _prepare_endpoint_call(
            endpoint, path_args, path_kwargs, body
        )
        return await self._request(
            endpoint.method,
            path,
            params=params,
            json=body,
            idempotency_key=idempotency_key,
            auth=auth,
            protocol=protocol,
        )

    async def _call_stream_endpoint(
        self,
        endpoint: _Endpoint,
        path_args: tuple[object, ...],
        path_kwargs: dict[str, object],
        *,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
    ) -> AsyncIterator[StreamEvent]:
        path, auth, protocol = _prepare_endpoint_call(
            endpoint, path_args, path_kwargs, body
        )
        async for event in self._stream(
            path, params=params, auth=auth, protocol=protocol
        ):
            yield event


def _make_sync_endpoint(endpoint: _Endpoint):
    def endpoint_method(
        self: HarnClient,
        *path_args: object,
        params: dict[str, Any] | None = None,
        body: JsonDict | None = None,
        idempotency_key: str | None = None,
        **path_kwargs: object,
    ) -> Any:
        return self._call_endpoint(
            endpoint,
            path_args,
            path_kwargs,
            params=params,
            body=body,
            idempotency_key=idempotency_key,
        )

    endpoint_method.__name__ = endpoint.name
    endpoint_method.__qualname__ = f"{HarnClient.__name__}.{endpoint.name}"
    endpoint_method.__doc__ = f"{endpoint.method} {endpoint.path}"
    endpoint_method.__signature__ = _endpoint_signature(endpoint)  # type: ignore[attr-defined]
    return endpoint_method


def _make_async_endpoint(endpoint: _Endpoint):
    if endpoint.stream:

        async def async_stream_endpoint_method(
            self: AsyncHarnClient,
            *path_args: object,
            params: dict[str, Any] | None = None,
            body: JsonDict | None = None,
            idempotency_key: str | None = None,
            **path_kwargs: object,
        ) -> AsyncIterator[StreamEvent]:
            async for event in self._call_stream_endpoint(
                endpoint,
                path_args,
                path_kwargs,
                params=params,
                body=body,
                idempotency_key=idempotency_key,
            ):
                yield event

        method = async_stream_endpoint_method
        signature = _endpoint_signature(endpoint).replace(
            return_annotation=AsyncIterator[StreamEvent]
        )
    else:

        async def async_endpoint_method(
            self: AsyncHarnClient,
            *path_args: object,
            params: dict[str, Any] | None = None,
            body: JsonDict | None = None,
            idempotency_key: str | None = None,
            **path_kwargs: object,
        ) -> Any:
            return await self._call_endpoint(
                endpoint,
                path_args,
                path_kwargs,
                params=params,
                body=body,
                idempotency_key=idempotency_key,
            )

        method = async_endpoint_method
        signature = _endpoint_signature(endpoint)

    method.__name__ = endpoint.name
    method.__qualname__ = f"{AsyncHarnClient.__name__}.{endpoint.name}"
    method.__doc__ = f"{endpoint.method} {endpoint.path}"
    method.__signature__ = signature  # type: ignore[attr-defined]
    return method


for _endpoint in _OPENAPI_ENDPOINTS:
    setattr(HarnClient, _endpoint.name, _make_sync_endpoint(_endpoint))
    setattr(AsyncHarnClient, _endpoint.name, _make_async_endpoint(_endpoint))
