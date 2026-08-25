from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.stream_events_harn_agents_protocol_version import (
    StreamEventsHarnAgentsProtocolVersion,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    workspace_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    task_id: str | Unset = UNSET,
    harn_agents_protocol_version: StreamEventsHarnAgentsProtocolVersion = StreamEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(last_event_id, Unset):
        headers["Last-Event-ID"] = last_event_id

    params: dict[str, Any] = {}

    params["workspace_id"] = workspace_id

    params["session_id"] = session_id

    params["task_id"] = task_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/events/stream",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | str:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | str]:
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
    task_id: str | Unset = UNSET,
    harn_agents_protocol_version: StreamEventsHarnAgentsProtocolVersion = StreamEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> Response[ErrorResponse | str]:
    """Stream global or filtered Events over Server-Sent Events.

    Args:
        workspace_id (str | Unset):
        session_id (str | Unset):
        task_id (str | Unset):
        harn_agents_protocol_version (StreamEventsHarnAgentsProtocolVersion):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        session_id=session_id,
        task_id=task_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
        last_event_id=last_event_id,
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
    task_id: str | Unset = UNSET,
    harn_agents_protocol_version: StreamEventsHarnAgentsProtocolVersion = StreamEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> ErrorResponse | str | None:
    """Stream global or filtered Events over Server-Sent Events.

    Args:
        workspace_id (str | Unset):
        session_id (str | Unset):
        task_id (str | Unset):
        harn_agents_protocol_version (StreamEventsHarnAgentsProtocolVersion):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | str
    """

    return sync_detailed(
        client=client,
        workspace_id=workspace_id,
        session_id=session_id,
        task_id=task_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
        last_event_id=last_event_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    workspace_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    task_id: str | Unset = UNSET,
    harn_agents_protocol_version: StreamEventsHarnAgentsProtocolVersion = StreamEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> Response[ErrorResponse | str]:
    """Stream global or filtered Events over Server-Sent Events.

    Args:
        workspace_id (str | Unset):
        session_id (str | Unset):
        task_id (str | Unset):
        harn_agents_protocol_version (StreamEventsHarnAgentsProtocolVersion):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        session_id=session_id,
        task_id=task_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
        last_event_id=last_event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    workspace_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    task_id: str | Unset = UNSET,
    harn_agents_protocol_version: StreamEventsHarnAgentsProtocolVersion = StreamEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> ErrorResponse | str | None:
    """Stream global or filtered Events over Server-Sent Events.

    Args:
        workspace_id (str | Unset):
        session_id (str | Unset):
        task_id (str | Unset):
        harn_agents_protocol_version (StreamEventsHarnAgentsProtocolVersion):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | str
    """

    return (
        await asyncio_detailed(
            client=client,
            workspace_id=workspace_id,
            session_id=session_id,
            task_id=task_id,
            harn_agents_protocol_version=harn_agents_protocol_version,
            last_event_id=last_event_id,
        )
    ).parsed
