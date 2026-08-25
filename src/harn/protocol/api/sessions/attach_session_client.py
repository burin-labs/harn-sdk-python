from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.attach_session_client_harn_agents_protocol_version import (
    AttachSessionClientHarnAgentsProtocolVersion,
)
from ...models.attach_session_client_request import AttachSessionClientRequest
from ...models.error_response import ErrorResponse
from ...models.live_session_client_change import LiveSessionClientChange
from ...types import UNSET, Response, Unset


def _get_kwargs(
    session_id: str,
    *,
    body: AttachSessionClientRequest,
    harn_agents_protocol_version: AttachSessionClientHarnAgentsProtocolVersion = AttachSessionClientHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/sessions/{session_id}/attach".format(
            session_id=quote(str(session_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | LiveSessionClientChange:
    if response.status_code == 200:
        response_200 = LiveSessionClientChange.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | LiveSessionClientChange]:
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
    body: AttachSessionClientRequest,
    harn_agents_protocol_version: AttachSessionClientHarnAgentsProtocolVersion = AttachSessionClientHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | LiveSessionClientChange]:
    """Attach a live client to a Session.

    Args:
        session_id (str):
        harn_agents_protocol_version (AttachSessionClientHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (AttachSessionClientRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LiveSessionClientChange]
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
    body: AttachSessionClientRequest,
    harn_agents_protocol_version: AttachSessionClientHarnAgentsProtocolVersion = AttachSessionClientHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | LiveSessionClientChange | None:
    """Attach a live client to a Session.

    Args:
        session_id (str):
        harn_agents_protocol_version (AttachSessionClientHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (AttachSessionClientRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LiveSessionClientChange
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
    body: AttachSessionClientRequest,
    harn_agents_protocol_version: AttachSessionClientHarnAgentsProtocolVersion = AttachSessionClientHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | LiveSessionClientChange]:
    """Attach a live client to a Session.

    Args:
        session_id (str):
        harn_agents_protocol_version (AttachSessionClientHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (AttachSessionClientRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LiveSessionClientChange]
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
    body: AttachSessionClientRequest,
    harn_agents_protocol_version: AttachSessionClientHarnAgentsProtocolVersion = AttachSessionClientHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | LiveSessionClientChange | None:
    """Attach a live client to a Session.

    Args:
        session_id (str):
        harn_agents_protocol_version (AttachSessionClientHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (AttachSessionClientRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LiveSessionClientChange
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
