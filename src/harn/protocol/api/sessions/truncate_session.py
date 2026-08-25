from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.truncate_session_harn_agents_protocol_version import (
    TruncateSessionHarnAgentsProtocolVersion,
)
from ...models.truncate_session_request import TruncateSessionRequest
from ...models.truncate_session_response import TruncateSessionResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    session_id: str,
    *,
    body: TruncateSessionRequest,
    harn_agents_protocol_version: TruncateSessionHarnAgentsProtocolVersion = TruncateSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/sessions/{session_id}/truncate".format(
            session_id=quote(str(session_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TruncateSessionResponse:
    if response.status_code == 200:
        response_200 = TruncateSessionResponse.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | TruncateSessionResponse]:
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
    body: TruncateSessionRequest,
    harn_agents_protocol_version: TruncateSessionHarnAgentsProtocolVersion = TruncateSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | TruncateSessionResponse]:
    """Truncate a Session transcript in place.

    Args:
        session_id (str):
        harn_agents_protocol_version (TruncateSessionHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (TruncateSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TruncateSessionResponse]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TruncateSessionRequest,
    harn_agents_protocol_version: TruncateSessionHarnAgentsProtocolVersion = TruncateSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | TruncateSessionResponse | None:
    """Truncate a Session transcript in place.

    Args:
        session_id (str):
        harn_agents_protocol_version (TruncateSessionHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (TruncateSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TruncateSessionResponse
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TruncateSessionRequest,
    harn_agents_protocol_version: TruncateSessionHarnAgentsProtocolVersion = TruncateSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | TruncateSessionResponse]:
    """Truncate a Session transcript in place.

    Args:
        session_id (str):
        harn_agents_protocol_version (TruncateSessionHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (TruncateSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TruncateSessionResponse]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TruncateSessionRequest,
    harn_agents_protocol_version: TruncateSessionHarnAgentsProtocolVersion = TruncateSessionHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | TruncateSessionResponse | None:
    """Truncate a Session transcript in place.

    Args:
        session_id (str):
        harn_agents_protocol_version (TruncateSessionHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (TruncateSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TruncateSessionResponse
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
