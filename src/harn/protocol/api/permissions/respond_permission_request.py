from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.permission_request import PermissionRequest
from ...models.permission_response_request import PermissionResponseRequest
from ...models.respond_permission_request_harn_agents_protocol_version import (
    RespondPermissionRequestHarnAgentsProtocolVersion,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    request_id: str,
    *,
    body: PermissionResponseRequest,
    harn_agents_protocol_version: RespondPermissionRequestHarnAgentsProtocolVersion = RespondPermissionRequestHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/permission-requests/{request_id}/respond".format(
            request_id=quote(str(request_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | PermissionRequest:
    if response.status_code == 200:
        response_200 = PermissionRequest.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | PermissionRequest]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    request_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PermissionResponseRequest,
    harn_agents_protocol_version: RespondPermissionRequestHarnAgentsProtocolVersion = RespondPermissionRequestHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | PermissionRequest]:
    """Approve or deny an ACP permission or HITL request.

     The local API forwards responses through the same runtime path as ACP
    `session/request_permission` or `harn.hitl.respond`, so decisions are
    captured by the active transcript, EventLog, replay, and receipt flows.

    Args:
        request_id (str):
        harn_agents_protocol_version (RespondPermissionRequestHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (PermissionResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PermissionRequest]
    """

    kwargs = _get_kwargs(
        request_id=request_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    request_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PermissionResponseRequest,
    harn_agents_protocol_version: RespondPermissionRequestHarnAgentsProtocolVersion = RespondPermissionRequestHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | PermissionRequest | None:
    """Approve or deny an ACP permission or HITL request.

     The local API forwards responses through the same runtime path as ACP
    `session/request_permission` or `harn.hitl.respond`, so decisions are
    captured by the active transcript, EventLog, replay, and receipt flows.

    Args:
        request_id (str):
        harn_agents_protocol_version (RespondPermissionRequestHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (PermissionResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PermissionRequest
    """

    return sync_detailed(
        request_id=request_id,
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    request_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PermissionResponseRequest,
    harn_agents_protocol_version: RespondPermissionRequestHarnAgentsProtocolVersion = RespondPermissionRequestHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | PermissionRequest]:
    """Approve or deny an ACP permission or HITL request.

     The local API forwards responses through the same runtime path as ACP
    `session/request_permission` or `harn.hitl.respond`, so decisions are
    captured by the active transcript, EventLog, replay, and receipt flows.

    Args:
        request_id (str):
        harn_agents_protocol_version (RespondPermissionRequestHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (PermissionResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PermissionRequest]
    """

    kwargs = _get_kwargs(
        request_id=request_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    request_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PermissionResponseRequest,
    harn_agents_protocol_version: RespondPermissionRequestHarnAgentsProtocolVersion = RespondPermissionRequestHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | PermissionRequest | None:
    """Approve or deny an ACP permission or HITL request.

     The local API forwards responses through the same runtime path as ACP
    `session/request_permission` or `harn.hitl.respond`, so decisions are
    captured by the active transcript, EventLog, replay, and receipt flows.

    Args:
        request_id (str):
        harn_agents_protocol_version (RespondPermissionRequestHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (PermissionResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PermissionRequest
    """

    return (
        await asyncio_detailed(
            request_id=request_id,
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
