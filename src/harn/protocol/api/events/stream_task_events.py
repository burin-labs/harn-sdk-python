from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.stream_task_events_harn_agents_protocol_version import (
    StreamTaskEventsHarnAgentsProtocolVersion,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    task_id: str,
    *,
    harn_agents_protocol_version: StreamTaskEventsHarnAgentsProtocolVersion = StreamTaskEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(last_event_id, Unset):
        headers["Last-Event-ID"] = last_event_id

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tasks/{task_id}/stream".format(
            task_id=quote(str(task_id), safe=""),
        ),
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
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: StreamTaskEventsHarnAgentsProtocolVersion = StreamTaskEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> Response[ErrorResponse | str]:
    """Stream Task Events over Server-Sent Events.

     WebSocket upgrades may use the same path for host-mediated interactive flows.

    Args:
        task_id (str):
        harn_agents_protocol_version (StreamTaskEventsHarnAgentsProtocolVersion):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
        last_event_id=last_event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: StreamTaskEventsHarnAgentsProtocolVersion = StreamTaskEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> ErrorResponse | str | None:
    """Stream Task Events over Server-Sent Events.

     WebSocket upgrades may use the same path for host-mediated interactive flows.

    Args:
        task_id (str):
        harn_agents_protocol_version (StreamTaskEventsHarnAgentsProtocolVersion):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | str
    """

    return sync_detailed(
        task_id=task_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
        last_event_id=last_event_id,
    ).parsed


async def asyncio_detailed(
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: StreamTaskEventsHarnAgentsProtocolVersion = StreamTaskEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> Response[ErrorResponse | str]:
    """Stream Task Events over Server-Sent Events.

     WebSocket upgrades may use the same path for host-mediated interactive flows.

    Args:
        task_id (str):
        harn_agents_protocol_version (StreamTaskEventsHarnAgentsProtocolVersion):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
        last_event_id=last_event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: StreamTaskEventsHarnAgentsProtocolVersion = StreamTaskEventsHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    last_event_id: str | Unset = UNSET,
) -> ErrorResponse | str | None:
    """Stream Task Events over Server-Sent Events.

     WebSocket upgrades may use the same path for host-mediated interactive flows.

    Args:
        task_id (str):
        harn_agents_protocol_version (StreamTaskEventsHarnAgentsProtocolVersion):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | str
    """

    return (
        await asyncio_detailed(
            task_id=task_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
            last_event_id=last_event_id,
        )
    ).parsed
