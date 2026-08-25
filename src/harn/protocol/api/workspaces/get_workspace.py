from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_workspace_harn_agents_protocol_version import (
    GetWorkspaceHarnAgentsProtocolVersion,
)
from ...models.workspace import Workspace
from ...types import Response


def _get_kwargs(
    workspace_id: str,
    *,
    harn_agents_protocol_version: GetWorkspaceHarnAgentsProtocolVersion = GetWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/workspaces/{workspace_id}".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

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
    harn_agents_protocol_version: GetWorkspaceHarnAgentsProtocolVersion = GetWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Workspace]:
    """Retrieve a Workspace.

    Args:
        workspace_id (str):
        harn_agents_protocol_version (GetWorkspaceHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Workspace]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetWorkspaceHarnAgentsProtocolVersion = GetWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Workspace | None:
    """Retrieve a Workspace.

    Args:
        workspace_id (str):
        harn_agents_protocol_version (GetWorkspaceHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Workspace
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetWorkspaceHarnAgentsProtocolVersion = GetWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Workspace]:
    """Retrieve a Workspace.

    Args:
        workspace_id (str):
        harn_agents_protocol_version (GetWorkspaceHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Workspace]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetWorkspaceHarnAgentsProtocolVersion = GetWorkspaceHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Workspace | None:
    """Retrieve a Workspace.

    Args:
        workspace_id (str):
        harn_agents_protocol_version (GetWorkspaceHarnAgentsProtocolVersion):

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
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
