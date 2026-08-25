from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_message_harn_agents_protocol_version import (
    GetMessageHarnAgentsProtocolVersion,
)
from ...models.message import Message
from ...types import Response


def _get_kwargs(
    message_id: str,
    *,
    harn_agents_protocol_version: GetMessageHarnAgentsProtocolVersion = GetMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/messages/{message_id}".format(
            message_id=quote(str(message_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Message:
    if response.status_code == 200:
        response_200 = Message.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Message]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetMessageHarnAgentsProtocolVersion = GetMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Message]:
    """Retrieve a Message.

    Args:
        message_id (str):
        harn_agents_protocol_version (GetMessageHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Message]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetMessageHarnAgentsProtocolVersion = GetMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Message | None:
    """Retrieve a Message.

    Args:
        message_id (str):
        harn_agents_protocol_version (GetMessageHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Message
    """

    return sync_detailed(
        message_id=message_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetMessageHarnAgentsProtocolVersion = GetMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Message]:
    """Retrieve a Message.

    Args:
        message_id (str):
        harn_agents_protocol_version (GetMessageHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Message]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetMessageHarnAgentsProtocolVersion = GetMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Message | None:
    """Retrieve a Message.

    Args:
        message_id (str):
        harn_agents_protocol_version (GetMessageHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Message
    """

    return (
        await asyncio_detailed(
            message_id=message_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
