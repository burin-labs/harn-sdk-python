import httpx
import pytest
from urllib.parse import quote

from harn import HARN_PROTOCOL_VERSION, ApiError, AsyncHarnClient, HarnClient
from harn.client import _OPENAPI_ENDPOINTS


EXPECTED_ENDPOINTS = (
    ("get_health", "GET", "/health"),
    ("get_version", "GET", "/version"),
    ("get_open_api_document", "GET", "/openapi.json"),
    ("get_protocol_discovery", "GET", "/v1"),
    ("get_runtime", "GET", "/v1/runtime"),
    ("list_capabilities", "GET", "/v1/capabilities"),
    ("list_tools", "GET", "/v1/tools"),
    ("get_tool", "GET", "/v1/tools/{tool_id}"),
    ("get_agent_card", "GET", "/v1/agent-card"),
    ("list_personas", "GET", "/v1/personas"),
    ("create_persona", "POST", "/v1/personas"),
    ("get_persona", "GET", "/v1/personas/{persona_id}"),
    ("update_persona", "PATCH", "/v1/personas/{persona_id}"),
    ("list_workspaces", "GET", "/v1/workspaces"),
    ("create_workspace", "POST", "/v1/workspaces"),
    ("get_workspace", "GET", "/v1/workspaces/{workspace_id}"),
    ("update_workspace", "PATCH", "/v1/workspaces/{workspace_id}"),
    ("read_workspace_file", "GET", "/v1/workspaces/{workspace_id}/files"),
    ("write_workspace_file", "PUT", "/v1/workspaces/{workspace_id}/files"),
    ("list_sessions", "GET", "/v1/sessions"),
    ("create_session", "POST", "/v1/sessions"),
    ("get_session", "GET", "/v1/sessions/{session_id}"),
    ("update_session", "PATCH", "/v1/sessions/{session_id}"),
    ("close_session", "POST", "/v1/sessions/{session_id}/close"),
    ("fork_session", "POST", "/v1/sessions/{session_id}/fork"),
    ("truncate_session", "POST", "/v1/sessions/{session_id}/truncate"),
    ("list_session_messages", "GET", "/v1/sessions/{session_id}/messages"),
    ("append_session_message", "POST", "/v1/sessions/{session_id}/messages"),
    ("list_session_tasks", "GET", "/v1/sessions/{session_id}/tasks"),
    ("submit_session_task", "POST", "/v1/sessions/{session_id}/tasks"),
    ("list_session_branches", "GET", "/v1/sessions/{session_id}/branches"),
    ("create_session_branch", "POST", "/v1/sessions/{session_id}/branches"),
    ("list_session_events", "GET", "/v1/sessions/{session_id}/events"),
    (
        "stream_session_events",
        "GET",
        "/v1/sessions/{session_id}/events/stream",
    ),
    ("list_tasks", "GET", "/v1/tasks"),
    ("submit_task", "POST", "/v1/tasks"),
    ("get_task", "GET", "/v1/tasks/{task_id}"),
    ("cancel_task", "POST", "/v1/tasks/{task_id}/cancel"),
    ("list_permission_requests", "GET", "/v1/permission-requests"),
    (
        "list_task_permission_requests",
        "GET",
        "/v1/tasks/{task_id}/permission-requests",
    ),
    (
        "respond_permission_request",
        "POST",
        "/v1/permission-requests/{request_id}/respond",
    ),
    ("replay_task", "POST", "/v1/tasks/{task_id}/replay"),
    ("append_task_message", "POST", "/v1/tasks/{task_id}/messages"),
    ("list_task_events", "GET", "/v1/tasks/{task_id}/events"),
    ("stream_task_events", "GET", "/v1/tasks/{task_id}/stream"),
    ("list_task_receipts", "GET", "/v1/tasks/{task_id}/receipts"),
    ("get_branch", "GET", "/v1/branches/{branch_id}"),
    ("get_message", "GET", "/v1/messages/{message_id}"),
    ("list_artifacts", "GET", "/v1/artifacts"),
    ("register_artifact", "POST", "/v1/artifacts"),
    ("get_artifact", "GET", "/v1/artifacts/{artifact_id}"),
    ("download_artifact_content", "GET", "/v1/artifacts/{artifact_id}/content"),
    ("list_events", "GET", "/v1/events"),
    ("get_event", "GET", "/v1/events/{event_id}"),
    ("stream_events", "GET", "/v1/events/stream"),
    ("get_receipt", "GET", "/v1/receipts/{receipt_id}"),
    ("verify_receipt", "POST", "/v1/receipts/{receipt_id}/verify"),
    ("list_memories", "GET", "/v1/memories"),
    ("create_memory", "POST", "/v1/memories"),
    ("get_memory", "GET", "/v1/memories/{memory_id}"),
    ("delete_memory", "DELETE", "/v1/memories/{memory_id}"),
    ("list_vaults", "GET", "/v1/vaults"),
    ("create_vault", "POST", "/v1/vaults"),
    ("get_vault", "GET", "/v1/vaults/{vault_id}"),
    ("list_connectors", "GET", "/v1/connectors"),
    ("get_connector", "GET", "/v1/connectors/{connector_id}"),
    ("list_skills", "GET", "/v1/skills"),
    ("get_skill", "GET", "/v1/skills/{skill_id}"),
    ("list_outcomes", "GET", "/v1/outcomes"),
    ("get_outcome", "GET", "/v1/outcomes/{outcome_id}"),
    ("list_quotas", "GET", "/v1/quotas"),
    ("get_quota", "GET", "/v1/quotas/{quota_id}"),
)


def test_client_surface_matches_latest_harn_openapi() -> None:
    actual = tuple((item.name, item.method, item.path) for item in _OPENAPI_ENDPOINTS)
    assert actual == EXPECTED_ENDPOINTS
    for name, _method, _path in EXPECTED_ENDPOINTS:
        assert callable(getattr(HarnClient, name))
        assert callable(getattr(AsyncHarnClient, name))

    assert not hasattr(HarnClient, "suspend_task")
    assert not hasattr(HarnClient, "list_context_packs")


def test_all_generated_endpoint_helpers_dispatch_expected_routes() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(
            {
                "method": request.method,
                "path": request.url.raw_path.decode(),
                "has_auth": "authorization" in request.headers,
                "has_protocol": "harn-agents-protocol-version" in request.headers,
            }
        )
        if request.url.path.endswith("/stream"):
            return httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=b'data: {"ok": true}\n\n',
            )
        if request.method == "DELETE":
            return httpx.Response(204)
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com"),
        token="token-123",
    ) as client:
        for endpoint in _OPENAPI_ENDPOINTS:
            args = [f"{name}/value" for name in endpoint.path_params]
            kwargs = {"body": {"ok": True}} if endpoint.accepts_body else {}
            result = getattr(client, endpoint.name)(*args, **kwargs)
            if endpoint.stream:
                assert [event.data for event in result] == [{"ok": True}]

    expected = []
    for endpoint in _OPENAPI_ENDPOINTS:
        path = endpoint.path
        for name in endpoint.path_params:
            path = path.replace(f"{{{name}}}", quote(f"{name}/value", safe=""))
        expected.append(
            {
                "method": endpoint.method,
                "path": path,
                "has_auth": not endpoint.public,
                "has_protocol": not endpoint.public,
            }
        )
    assert seen == expected


def test_client_adds_auth_header() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer token-123"
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com"),
        token="token-123",
    ) as client:
        response = client.list_sessions()
    assert response == {"ok": True}


def test_client_adds_current_protocol_header_to_v1_calls() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["harn-agents-protocol-version"] == HARN_PROTOCOL_VERSION
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        response = client.list_sessions()
    assert response == {"ok": True}


def test_public_discovery_omits_protocol_and_auth_headers(monkeypatch) -> None:
    monkeypatch.setenv("HARN_API_KEY", "ambient-token")
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["has_protocol"] = "harn-agents-protocol-version" in request.headers
        seen["has_auth"] = "authorization" in request.headers
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com"),
        token="direct-token",
    ) as client:
        response = client.get_agent_card()
    assert response == {"ok": True}
    assert seen["has_protocol"] is False
    assert seen["has_auth"] is False


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


def test_current_endpoint_helpers_escape_path_segments_and_idempotency() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(
            {
                "method": request.method,
                "path": request.url.raw_path.decode(),
                "body": request.read(),
                "idempotency": request.headers["idempotency-key"],
            }
        )
        if request.method == "DELETE":
            return httpx.Response(204)
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        response = client.write_workspace_file(
            "workspace/1",
            params={"path": "notes/today.txt"},
            body={"content": "hello"},
            idempotency_key="idem-1",
        )
        deleted = client.delete_memory("mem/1", idempotency_key="idem-2")
    assert response == {"ok": True}
    assert deleted is None
    assert seen == [
        {
            "method": "PUT",
            "path": "/v1/workspaces/workspace%2F1/files?path=notes%2Ftoday.txt",
            "body": b'{"content":"hello"}',
            "idempotency": "idem-1",
        },
        {
            "method": "DELETE",
            "path": "/v1/memories/mem%2F1",
            "body": b"",
            "idempotency": "idem-2",
        },
    ]


def test_request_escape_hatch_reaches_unwrapped_cloud_endpoints() -> None:
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["path"] = request.url.path
        seen["query"] = request.url.query.decode()
        return httpx.Response(204)

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        response = client.request(
            "PATCH",
            "/v1/remote-attach/policy",
            params={"enabled": True},
        )
    assert response is None
    assert seen == {
        "method": "PATCH",
        "path": "/v1/remote-attach/policy",
        "query": "enabled=true",
    }


@pytest.mark.asyncio
async def test_async_client_shares_response_and_header_behavior() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["harn-agents-protocol-version"] == HARN_PROTOCOL_VERSION
        return httpx.Response(200, json={"events": []})

    transport = httpx.MockTransport(handler)
    async with AsyncHarnClient(
        client=httpx.AsyncClient(
            transport=transport, base_url="https://api.harnlang.com"
        )
    ) as client:
        response = await client.list_events()
    assert response == {"events": []}


def test_stream_errors_raise_api_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            json={"error": {"code": "forbidden", "message": "No access"}},
        )

    transport = httpx.MockTransport(handler)
    with HarnClient(
        client=httpx.Client(transport=transport, base_url="https://api.harnlang.com")
    ) as client:
        with pytest.raises(ApiError) as exc_info:
            list(client.stream_events())

    assert exc_info.value.status_code == 403
    assert exc_info.value.error is not None
    assert exc_info.value.error.code == "forbidden"
