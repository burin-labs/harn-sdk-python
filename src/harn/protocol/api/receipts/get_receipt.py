from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_receipt_harn_agents_protocol_version import (
    GetReceiptHarnAgentsProtocolVersion,
)
from ...models.receipt import Receipt
from ...types import Response


def _get_kwargs(
    receipt_id: str,
    *,
    harn_agents_protocol_version: GetReceiptHarnAgentsProtocolVersion = GetReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/receipts/{receipt_id}".format(
            receipt_id=quote(str(receipt_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Receipt:
    if response.status_code == 200:
        response_200 = Receipt.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Receipt]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    receipt_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetReceiptHarnAgentsProtocolVersion = GetReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Receipt]:
    """Retrieve a Receipt resource.

    Args:
        receipt_id (str):
        harn_agents_protocol_version (GetReceiptHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Receipt]
    """

    kwargs = _get_kwargs(
        receipt_id=receipt_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    receipt_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetReceiptHarnAgentsProtocolVersion = GetReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Receipt | None:
    """Retrieve a Receipt resource.

    Args:
        receipt_id (str):
        harn_agents_protocol_version (GetReceiptHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Receipt
    """

    return sync_detailed(
        receipt_id=receipt_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    receipt_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetReceiptHarnAgentsProtocolVersion = GetReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Receipt]:
    """Retrieve a Receipt resource.

    Args:
        receipt_id (str):
        harn_agents_protocol_version (GetReceiptHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Receipt]
    """

    kwargs = _get_kwargs(
        receipt_id=receipt_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    receipt_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetReceiptHarnAgentsProtocolVersion = GetReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Receipt | None:
    """Retrieve a Receipt resource.

    Args:
        receipt_id (str):
        harn_agents_protocol_version (GetReceiptHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Receipt
    """

    return (
        await asyncio_detailed(
            receipt_id=receipt_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
