from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.audit_entry_list import AuditEntryList
from ...models.error_response import ErrorResponse
from ...models.get_permission_history_harn_agents_protocol_version import (
    GetPermissionHistoryHarnAgentsProtocolVersion,
)
from ...models.get_permission_history_outcome import GetPermissionHistoryOutcome
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    session_id: str | Unset = UNSET,
    workspace_id: str | Unset = UNSET,
    tenant_id: str | Unset = UNSET,
    actor: str | Unset = UNSET,
    outcome: GetPermissionHistoryOutcome | Unset = UNSET,
    limit: int | Unset = 50,
    harn_agents_protocol_version: GetPermissionHistoryHarnAgentsProtocolVersion = GetPermissionHistoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    params: dict[str, Any] = {}

    params["session_id"] = session_id

    params["workspace_id"] = workspace_id

    params["tenant_id"] = tenant_id

    params["actor"] = actor

    json_outcome: str | Unset = UNSET
    if not isinstance(outcome, Unset):
        json_outcome = outcome.value

    params["outcome"] = json_outcome

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/permissions/history",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AuditEntryList | ErrorResponse:
    if response.status_code == 200:
        response_200 = AuditEntryList.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AuditEntryList | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    session_id: str | Unset = UNSET,
    workspace_id: str | Unset = UNSET,
    tenant_id: str | Unset = UNSET,
    actor: str | Unset = UNSET,
    outcome: GetPermissionHistoryOutcome | Unset = UNSET,
    limit: int | Unset = 50,
    harn_agents_protocol_version: GetPermissionHistoryHarnAgentsProtocolVersion = GetPermissionHistoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[AuditEntryList | ErrorResponse]:
    """Query the permission audit log.

     Returns audit entries (every grant, deny, escalation) in
    reverse-chronological order. Filter by session, workspace,
    tenant, actor, or outcome. The in-memory store currently
    retains the last `audit_capacity` entries; durable backends
    (A.5) will eventually replace this with the session-store
    event feed.

    Args:
        session_id (str | Unset):
        workspace_id (str | Unset):
        tenant_id (str | Unset):
        actor (str | Unset):
        outcome (GetPermissionHistoryOutcome | Unset):
        limit (int | Unset):  Default: 50.
        harn_agents_protocol_version (GetPermissionHistoryHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditEntryList | ErrorResponse]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        workspace_id=workspace_id,
        tenant_id=tenant_id,
        actor=actor,
        outcome=outcome,
        limit=limit,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    session_id: str | Unset = UNSET,
    workspace_id: str | Unset = UNSET,
    tenant_id: str | Unset = UNSET,
    actor: str | Unset = UNSET,
    outcome: GetPermissionHistoryOutcome | Unset = UNSET,
    limit: int | Unset = 50,
    harn_agents_protocol_version: GetPermissionHistoryHarnAgentsProtocolVersion = GetPermissionHistoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> AuditEntryList | ErrorResponse | None:
    """Query the permission audit log.

     Returns audit entries (every grant, deny, escalation) in
    reverse-chronological order. Filter by session, workspace,
    tenant, actor, or outcome. The in-memory store currently
    retains the last `audit_capacity` entries; durable backends
    (A.5) will eventually replace this with the session-store
    event feed.

    Args:
        session_id (str | Unset):
        workspace_id (str | Unset):
        tenant_id (str | Unset):
        actor (str | Unset):
        outcome (GetPermissionHistoryOutcome | Unset):
        limit (int | Unset):  Default: 50.
        harn_agents_protocol_version (GetPermissionHistoryHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditEntryList | ErrorResponse
    """

    return sync_detailed(
        client=client,
        session_id=session_id,
        workspace_id=workspace_id,
        tenant_id=tenant_id,
        actor=actor,
        outcome=outcome,
        limit=limit,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    session_id: str | Unset = UNSET,
    workspace_id: str | Unset = UNSET,
    tenant_id: str | Unset = UNSET,
    actor: str | Unset = UNSET,
    outcome: GetPermissionHistoryOutcome | Unset = UNSET,
    limit: int | Unset = 50,
    harn_agents_protocol_version: GetPermissionHistoryHarnAgentsProtocolVersion = GetPermissionHistoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[AuditEntryList | ErrorResponse]:
    """Query the permission audit log.

     Returns audit entries (every grant, deny, escalation) in
    reverse-chronological order. Filter by session, workspace,
    tenant, actor, or outcome. The in-memory store currently
    retains the last `audit_capacity` entries; durable backends
    (A.5) will eventually replace this with the session-store
    event feed.

    Args:
        session_id (str | Unset):
        workspace_id (str | Unset):
        tenant_id (str | Unset):
        actor (str | Unset):
        outcome (GetPermissionHistoryOutcome | Unset):
        limit (int | Unset):  Default: 50.
        harn_agents_protocol_version (GetPermissionHistoryHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditEntryList | ErrorResponse]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        workspace_id=workspace_id,
        tenant_id=tenant_id,
        actor=actor,
        outcome=outcome,
        limit=limit,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    session_id: str | Unset = UNSET,
    workspace_id: str | Unset = UNSET,
    tenant_id: str | Unset = UNSET,
    actor: str | Unset = UNSET,
    outcome: GetPermissionHistoryOutcome | Unset = UNSET,
    limit: int | Unset = 50,
    harn_agents_protocol_version: GetPermissionHistoryHarnAgentsProtocolVersion = GetPermissionHistoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> AuditEntryList | ErrorResponse | None:
    """Query the permission audit log.

     Returns audit entries (every grant, deny, escalation) in
    reverse-chronological order. Filter by session, workspace,
    tenant, actor, or outcome. The in-memory store currently
    retains the last `audit_capacity` entries; durable backends
    (A.5) will eventually replace this with the session-store
    event feed.

    Args:
        session_id (str | Unset):
        workspace_id (str | Unset):
        tenant_id (str | Unset):
        actor (str | Unset):
        outcome (GetPermissionHistoryOutcome | Unset):
        limit (int | Unset):  Default: 50.
        harn_agents_protocol_version (GetPermissionHistoryHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditEntryList | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            session_id=session_id,
            workspace_id=workspace_id,
            tenant_id=tenant_id,
            actor=actor,
            outcome=outcome,
            limit=limit,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
