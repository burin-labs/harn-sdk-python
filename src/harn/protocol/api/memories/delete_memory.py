from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.delete_memory_harn_agents_protocol_version import (
    DeleteMemoryHarnAgentsProtocolVersion,
)
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    memory_id: str,
    *,
    harn_agents_protocol_version: DeleteMemoryHarnAgentsProtocolVersion = DeleteMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/memories/{memory_id}".format(
            memory_id=quote(str(memory_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ErrorResponse:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    memory_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: DeleteMemoryHarnAgentsProtocolVersion = DeleteMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[Any | ErrorResponse]:
    """Delete or tombstone a Memory record.

    Args:
        memory_id (str):
        harn_agents_protocol_version (DeleteMemoryHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        memory_id=memory_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    memory_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: DeleteMemoryHarnAgentsProtocolVersion = DeleteMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Any | ErrorResponse | None:
    """Delete or tombstone a Memory record.

    Args:
        memory_id (str):
        harn_agents_protocol_version (DeleteMemoryHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return sync_detailed(
        memory_id=memory_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    memory_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: DeleteMemoryHarnAgentsProtocolVersion = DeleteMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[Any | ErrorResponse]:
    """Delete or tombstone a Memory record.

    Args:
        memory_id (str):
        harn_agents_protocol_version (DeleteMemoryHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        memory_id=memory_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    memory_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: DeleteMemoryHarnAgentsProtocolVersion = DeleteMemoryHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Any | ErrorResponse | None:
    """Delete or tombstone a Memory record.

    Args:
        memory_id (str):
        harn_agents_protocol_version (DeleteMemoryHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            memory_id=memory_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
