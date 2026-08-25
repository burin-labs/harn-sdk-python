from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.receipt_verification import ReceiptVerification
from ...models.verify_receipt_harn_agents_protocol_version import (
    VerifyReceiptHarnAgentsProtocolVersion,
)
from ...models.verify_receipt_request import VerifyReceiptRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    receipt_id: str,
    *,
    body: VerifyReceiptRequest | Unset = UNSET,
    harn_agents_protocol_version: VerifyReceiptHarnAgentsProtocolVersion = VerifyReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/receipts/{receipt_id}/verify".format(
            receipt_id=quote(str(receipt_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ReceiptVerification:
    if response.status_code == 200:
        response_200 = ReceiptVerification.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | ReceiptVerification]:
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
    body: VerifyReceiptRequest | Unset = UNSET,
    harn_agents_protocol_version: VerifyReceiptHarnAgentsProtocolVersion = VerifyReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | ReceiptVerification]:
    """Verify a Receipt.

    Args:
        receipt_id (str):
        harn_agents_protocol_version (VerifyReceiptHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (VerifyReceiptRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ReceiptVerification]
    """

    kwargs = _get_kwargs(
        receipt_id=receipt_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    receipt_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: VerifyReceiptRequest | Unset = UNSET,
    harn_agents_protocol_version: VerifyReceiptHarnAgentsProtocolVersion = VerifyReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | ReceiptVerification | None:
    """Verify a Receipt.

    Args:
        receipt_id (str):
        harn_agents_protocol_version (VerifyReceiptHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (VerifyReceiptRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ReceiptVerification
    """

    return sync_detailed(
        receipt_id=receipt_id,
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    receipt_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: VerifyReceiptRequest | Unset = UNSET,
    harn_agents_protocol_version: VerifyReceiptHarnAgentsProtocolVersion = VerifyReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | ReceiptVerification]:
    """Verify a Receipt.

    Args:
        receipt_id (str):
        harn_agents_protocol_version (VerifyReceiptHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (VerifyReceiptRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ReceiptVerification]
    """

    kwargs = _get_kwargs(
        receipt_id=receipt_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    receipt_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: VerifyReceiptRequest | Unset = UNSET,
    harn_agents_protocol_version: VerifyReceiptHarnAgentsProtocolVersion = VerifyReceiptHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | ReceiptVerification | None:
    """Verify a Receipt.

    Args:
        receipt_id (str):
        harn_agents_protocol_version (VerifyReceiptHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (VerifyReceiptRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ReceiptVerification
    """

    return (
        await asyncio_detailed(
            receipt_id=receipt_id,
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
