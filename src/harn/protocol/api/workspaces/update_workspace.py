from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.update_workspace_harn_agents_protocol_version import (
    UpdateWorkspaceHarnAgentsProtocolVersion,
)
from ...models.update_workspace_request import UpdateWorkspaceRequest
from ...models.workspace import Workspace
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: str,
    *,
    body: UpdateWorkspaceRequest,
    harn_agents_protocol_version: UpdateWorkspaceHarnAgentsProtocolVersion = UpdateWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/workspaces/{workspace_id}".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Workspace:
    if response.status_code == 200:
        response_200 = Workspace.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Workspace]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateWorkspaceRequest,
    harn_agents_protocol_version: UpdateWorkspaceHarnAgentsProtocolVersion = UpdateWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Workspace]:
    """Update mutable Workspace metadata and policy links.

    Args:
        workspace_id (str):
        harn_agents_protocol_version (UpdateWorkspaceHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (UpdateWorkspaceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Workspace]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateWorkspaceRequest,
    harn_agents_protocol_version: UpdateWorkspaceHarnAgentsProtocolVersion = UpdateWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Workspace | None:
    """Update mutable Workspace metadata and policy links.

    Args:
        workspace_id (str):
        harn_agents_protocol_version (UpdateWorkspaceHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (UpdateWorkspaceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Workspace
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateWorkspaceRequest,
    harn_agents_protocol_version: UpdateWorkspaceHarnAgentsProtocolVersion = UpdateWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Workspace]:
    """Update mutable Workspace metadata and policy links.

    Args:
        workspace_id (str):
        harn_agents_protocol_version (UpdateWorkspaceHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (UpdateWorkspaceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Workspace]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateWorkspaceRequest,
    harn_agents_protocol_version: UpdateWorkspaceHarnAgentsProtocolVersion = UpdateWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Workspace | None:
    """Update mutable Workspace metadata and policy links.

    Args:
        workspace_id (str):
        harn_agents_protocol_version (UpdateWorkspaceHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (UpdateWorkspaceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Workspace
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
