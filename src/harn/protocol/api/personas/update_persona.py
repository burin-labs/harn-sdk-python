from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.persona import Persona
from ...models.update_persona_harn_agents_protocol_version import (
    UpdatePersonaHarnAgentsProtocolVersion,
)
from ...models.update_persona_request import UpdatePersonaRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    persona_id: str,
    *,
    body: UpdatePersonaRequest,
    harn_agents_protocol_version: UpdatePersonaHarnAgentsProtocolVersion = UpdatePersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/personas/{persona_id}".format(
            persona_id=quote(str(persona_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

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
    body: UpdatePersonaRequest,
    harn_agents_protocol_version: UpdatePersonaHarnAgentsProtocolVersion = UpdatePersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Persona]:
    """Update mutable Persona metadata and policy links.

    Args:
        persona_id (str):
        harn_agents_protocol_version (UpdatePersonaHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (UpdatePersonaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Persona]
    """

    kwargs = _get_kwargs(
        persona_id=persona_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    persona_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdatePersonaRequest,
    harn_agents_protocol_version: UpdatePersonaHarnAgentsProtocolVersion = UpdatePersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Persona | None:
    """Update mutable Persona metadata and policy links.

    Args:
        persona_id (str):
        harn_agents_protocol_version (UpdatePersonaHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (UpdatePersonaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Persona
    """

    return sync_detailed(
        persona_id=persona_id,
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    persona_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdatePersonaRequest,
    harn_agents_protocol_version: UpdatePersonaHarnAgentsProtocolVersion = UpdatePersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Persona]:
    """Update mutable Persona metadata and policy links.

    Args:
        persona_id (str):
        harn_agents_protocol_version (UpdatePersonaHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (UpdatePersonaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Persona]
    """

    kwargs = _get_kwargs(
        persona_id=persona_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    persona_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdatePersonaRequest,
    harn_agents_protocol_version: UpdatePersonaHarnAgentsProtocolVersion = UpdatePersonaHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Persona | None:
    """Update mutable Persona metadata and policy links.

    Args:
        persona_id (str):
        harn_agents_protocol_version (UpdatePersonaHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (UpdatePersonaRequest):

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
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
