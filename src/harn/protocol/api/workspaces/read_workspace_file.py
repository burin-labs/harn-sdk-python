from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.read_workspace_file_harn_agents_protocol_version import (
    ReadWorkspaceFileHarnAgentsProtocolVersion,
)
from ...models.workspace_file import WorkspaceFile
from ...models.workspace_file_listing import WorkspaceFileListing
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: str,
    *,
    path: str | Unset = UNSET,
    harn_agents_protocol_version: ReadWorkspaceFileHarnAgentsProtocolVersion = ReadWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    params: dict[str, Any] = {}

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/workspaces/{workspace_id}/files".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | WorkspaceFile | WorkspaceFileListing:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> WorkspaceFile | WorkspaceFileListing:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = WorkspaceFile.from_dict(data)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = WorkspaceFileListing.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | WorkspaceFile | WorkspaceFileListing]:
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
    path: str | Unset = UNSET,
    harn_agents_protocol_version: ReadWorkspaceFileHarnAgentsProtocolVersion = ReadWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | WorkspaceFile | WorkspaceFileListing]:
    """Read or list UTF-8 files under a Workspace root.

    Args:
        workspace_id (str):
        path (str | Unset):
        harn_agents_protocol_version (ReadWorkspaceFileHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WorkspaceFile | WorkspaceFileListing]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        path=path,
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
    path: str | Unset = UNSET,
    harn_agents_protocol_version: ReadWorkspaceFileHarnAgentsProtocolVersion = ReadWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | WorkspaceFile | WorkspaceFileListing | None:
    """Read or list UTF-8 files under a Workspace root.

    Args:
        workspace_id (str):
        path (str | Unset):
        harn_agents_protocol_version (ReadWorkspaceFileHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WorkspaceFile | WorkspaceFileListing
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        path=path,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    path: str | Unset = UNSET,
    harn_agents_protocol_version: ReadWorkspaceFileHarnAgentsProtocolVersion = ReadWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | WorkspaceFile | WorkspaceFileListing]:
    """Read or list UTF-8 files under a Workspace root.

    Args:
        workspace_id (str):
        path (str | Unset):
        harn_agents_protocol_version (ReadWorkspaceFileHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WorkspaceFile | WorkspaceFileListing]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        path=path,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    path: str | Unset = UNSET,
    harn_agents_protocol_version: ReadWorkspaceFileHarnAgentsProtocolVersion = ReadWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | WorkspaceFile | WorkspaceFileListing | None:
    """Read or list UTF-8 files under a Workspace root.

    Args:
        workspace_id (str):
        path (str | Unset):
        harn_agents_protocol_version (ReadWorkspaceFileHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WorkspaceFile | WorkspaceFileListing
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            path=path,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
