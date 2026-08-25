from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_session_messages_harn_agents_protocol_version import (
    ListSessionMessagesHarnAgentsProtocolVersion,
)
from ...models.message_list import MessageList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    session_id: str,
    *,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListSessionMessagesHarnAgentsProtocolVersion = ListSessionMessagesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sessions/{session_id}/messages".format(
            session_id=quote(str(session_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | MessageList:
    if response.status_code == 200:
        response_200 = MessageList.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | MessageList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListSessionMessagesHarnAgentsProtocolVersion = ListSessionMessagesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | MessageList]:
    """List Messages in a Session.

    Args:
        session_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        harn_agents_protocol_version (ListSessionMessagesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MessageList]
    """

    kwargs = _get_kwargs(
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
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListSessionMessagesHarnAgentsProtocolVersion = ListSessionMessagesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | MessageList | None:
    """List Messages in a Session.

    Args:
        session_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        harn_agents_protocol_version (ListSessionMessagesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MessageList
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        limit=limit,
        cursor=cursor,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListSessionMessagesHarnAgentsProtocolVersion = ListSessionMessagesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | MessageList]:
    """List Messages in a Session.

    Args:
        session_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        harn_agents_protocol_version (ListSessionMessagesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MessageList]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        limit=limit,
        cursor=cursor,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    harn_agents_protocol_version: ListSessionMessagesHarnAgentsProtocolVersion = ListSessionMessagesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | MessageList | None:
    """List Messages in a Session.

    Args:
        session_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        harn_agents_protocol_version (ListSessionMessagesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MessageList
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            limit=limit,
            cursor=cursor,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
