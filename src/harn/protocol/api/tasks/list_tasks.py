from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_tasks_harn_agents_protocol_version import (
    ListTasksHarnAgentsProtocolVersion,
)
from ...models.task_list import TaskList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    workspace_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListTasksHarnAgentsProtocolVersion = ListTasksHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    params: dict[str, Any] = {}

    params["workspace_id"] = workspace_id

    params["session_id"] = session_id

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tasks",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TaskList:
    if response.status_code == 200:
        response_200 = TaskList.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | TaskList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    workspace_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListTasksHarnAgentsProtocolVersion = ListTasksHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | TaskList]:
    """List Tasks visible to the caller.

    Args:
        workspace_id (str | Unset):
        session_id (str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        harn_agents_protocol_version (ListTasksHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TaskList]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        session_id=session_id,
        limit=limit,
        cursor=cursor,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    workspace_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListTasksHarnAgentsProtocolVersion = ListTasksHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | TaskList | None:
    """List Tasks visible to the caller.

    Args:
        workspace_id (str | Unset):
        session_id (str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        harn_agents_protocol_version (ListTasksHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TaskList
    """

    return sync_detailed(
        client=client,
        workspace_id=workspace_id,
        session_id=session_id,
        limit=limit,
        cursor=cursor,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    workspace_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListTasksHarnAgentsProtocolVersion = ListTasksHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | TaskList]:
    """List Tasks visible to the caller.

    Args:
        workspace_id (str | Unset):
        session_id (str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        harn_agents_protocol_version (ListTasksHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TaskList]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        session_id=session_id,
        limit=limit,
        cursor=cursor,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    workspace_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListTasksHarnAgentsProtocolVersion = ListTasksHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | TaskList | None:
    """List Tasks visible to the caller.

    Args:
        workspace_id (str | Unset):
        session_id (str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        harn_agents_protocol_version (ListTasksHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TaskList
    """

    return (
        await asyncio_detailed(
            client=client,
            workspace_id=workspace_id,
            session_id=session_id,
            limit=limit,
            cursor=cursor,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
