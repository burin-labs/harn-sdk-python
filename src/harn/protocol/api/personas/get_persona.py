from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_persona_harn_agents_protocol_version import (
    GetPersonaHarnAgentsProtocolVersion,
)
from ...models.persona import Persona
from ...types import Response


def _get_kwargs(
    persona_id: str,
    *,
    harn_agents_protocol_version: GetPersonaHarnAgentsProtocolVersion = GetPersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/personas/{persona_id}".format(
            persona_id=quote(str(persona_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Persona:
    if response.status_code == 200:
        response_200 = Persona.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Persona]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    persona_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetPersonaHarnAgentsProtocolVersion = GetPersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Persona]:
    """Retrieve a Persona.

    Args:
        persona_id (str):
        harn_agents_protocol_version (GetPersonaHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Persona]
    """

    kwargs = _get_kwargs(
        persona_id=persona_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    persona_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetPersonaHarnAgentsProtocolVersion = GetPersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Persona | None:
    """Retrieve a Persona.

    Args:
        persona_id (str):
        harn_agents_protocol_version (GetPersonaHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Persona
    """

    return sync_detailed(
        persona_id=persona_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    persona_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetPersonaHarnAgentsProtocolVersion = GetPersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Persona]:
    """Retrieve a Persona.

    Args:
        persona_id (str):
        harn_agents_protocol_version (GetPersonaHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Persona]
    """

    kwargs = _get_kwargs(
        persona_id=persona_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    persona_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetPersonaHarnAgentsProtocolVersion = GetPersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Persona | None:
    """Retrieve a Persona.

    Args:
        persona_id (str):
        harn_agents_protocol_version (GetPersonaHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Persona
    """

    return (
        await asyncio_detailed(
            persona_id=persona_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
