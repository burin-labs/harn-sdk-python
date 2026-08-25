from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.create_memory_harn_agents_protocol_version import (
    CreateMemoryHarnAgentsProtocolVersion,
)
from ...models.create_memory_request import CreateMemoryRequest
from ...models.error_response import ErrorResponse
from ...models.memory import Memory
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CreateMemoryRequest,
    harn_agents_protocol_version: CreateMemoryHarnAgentsProtocolVersion = CreateMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/memories",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Memory:
    if response.status_code == 201:
        response_201 = Memory.from_dict(response.json())

        return response_201

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Memory]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateMemoryRequest,
    harn_agents_protocol_version: CreateMemoryHarnAgentsProtocolVersion = CreateMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Memory]:
    """Create a durable Memory record.

    Args:
        harn_agents_protocol_version (CreateMemoryHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (CreateMemoryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Memory]
    """

    kwargs = _get_kwargs(
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: CreateMemoryRequest,
    harn_agents_protocol_version: CreateMemoryHarnAgentsProtocolVersion = CreateMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Memory | None:
    """Create a durable Memory record.

    Args:
        harn_agents_protocol_version (CreateMemoryHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (CreateMemoryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Memory
    """

    return sync_detailed(
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateMemoryRequest,
    harn_agents_protocol_version: CreateMemoryHarnAgentsProtocolVersion = CreateMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Memory]:
    """Create a durable Memory record.

    Args:
        harn_agents_protocol_version (CreateMemoryHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (CreateMemoryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Memory]
    """

    kwargs = _get_kwargs(
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateMemoryRequest,
    harn_agents_protocol_version: CreateMemoryHarnAgentsProtocolVersion = CreateMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Memory | None:
    """Create a durable Memory record.

    Args:
        harn_agents_protocol_version (CreateMemoryHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (CreateMemoryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Memory
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
