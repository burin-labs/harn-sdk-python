from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_session_harn_agents_protocol_version import (
    GetSessionHarnAgentsProtocolVersion,
)
from ...models.session import Session
from ...types import Response


def _get_kwargs(
    session_id: str,
    *,
    harn_agents_protocol_version: GetSessionHarnAgentsProtocolVersion = GetSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sessions/{session_id}".format(
            session_id=quote(str(session_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Session:
    if response.status_code == 200:
        response_200 = Session.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Session]:
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
    harn_agents_protocol_version: GetSessionHarnAgentsProtocolVersion = GetSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Session]:
    """Retrieve a Session.

    Args:
        session_id (str):
        harn_agents_protocol_version (GetSessionHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Session]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
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
    harn_agents_protocol_version: GetSessionHarnAgentsProtocolVersion = GetSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Session | None:
    """Retrieve a Session.

    Args:
        session_id (str):
        harn_agents_protocol_version (GetSessionHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Session
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetSessionHarnAgentsProtocolVersion = GetSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Session]:
    """Retrieve a Session.

    Args:
        session_id (str):
        harn_agents_protocol_version (GetSessionHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Session]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetSessionHarnAgentsProtocolVersion = GetSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Session | None:
    """Retrieve a Session.

    Args:
        session_id (str):
        harn_agents_protocol_version (GetSessionHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Session
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
