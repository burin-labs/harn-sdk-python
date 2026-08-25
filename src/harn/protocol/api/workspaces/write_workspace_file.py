from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.workspace_file import WorkspaceFile
from ...models.write_workspace_file_harn_agents_protocol_version import (
    WriteWorkspaceFileHarnAgentsProtocolVersion,
)
from ...models.write_workspace_file_request import WriteWorkspaceFileRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: str,
    *,
    body: WriteWorkspaceFileRequest,
    path: str | Unset = UNSET,
    harn_agents_protocol_version: WriteWorkspaceFileHarnAgentsProtocolVersion = WriteWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    params: dict[str, Any] = {}

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/workspaces/{workspace_id}/files".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | WorkspaceFile:
    if response.status_code == 200:
        response_200 = WorkspaceFile.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | WorkspaceFile]:
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
    body: WriteWorkspaceFileRequest,
    path: str | Unset = UNSET,
    harn_agents_protocol_version: WriteWorkspaceFileHarnAgentsProtocolVersion = WriteWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | WorkspaceFile]:
    """Write a UTF-8 file under a Workspace root.

    Args:
        workspace_id (str):
        path (str | Unset):
        harn_agents_protocol_version (WriteWorkspaceFileHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (WriteWorkspaceFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WorkspaceFile]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
        path=path,
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
    body: WriteWorkspaceFileRequest,
    path: str | Unset = UNSET,
    harn_agents_protocol_version: WriteWorkspaceFileHarnAgentsProtocolVersion = WriteWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | WorkspaceFile | None:
    """Write a UTF-8 file under a Workspace root.

    Args:
        workspace_id (str):
        path (str | Unset):
        harn_agents_protocol_version (WriteWorkspaceFileHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (WriteWorkspaceFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WorkspaceFile
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        body=body,
        path=path,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: WriteWorkspaceFileRequest,
    path: str | Unset = UNSET,
    harn_agents_protocol_version: WriteWorkspaceFileHarnAgentsProtocolVersion = WriteWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | WorkspaceFile]:
    """Write a UTF-8 file under a Workspace root.

    Args:
        workspace_id (str):
        path (str | Unset):
        harn_agents_protocol_version (WriteWorkspaceFileHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (WriteWorkspaceFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WorkspaceFile]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
        path=path,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: WriteWorkspaceFileRequest,
    path: str | Unset = UNSET,
    harn_agents_protocol_version: WriteWorkspaceFileHarnAgentsProtocolVersion = WriteWorkspaceFileHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | WorkspaceFile | None:
    """Write a UTF-8 file under a Workspace root.

    Args:
        workspace_id (str):
        path (str | Unset):
        harn_agents_protocol_version (WriteWorkspaceFileHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (WriteWorkspaceFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WorkspaceFile
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
            path=path,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
