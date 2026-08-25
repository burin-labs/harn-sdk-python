from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.cancel_task_harn_agents_protocol_version import (
    CancelTaskHarnAgentsProtocolVersion,
)
from ...models.cancel_task_request import CancelTaskRequest
from ...models.error import Error
from ...models.error_response import ErrorResponse
from ...models.task import Task
from ...types import UNSET, Response, Unset


def _get_kwargs(
    task_id: str,
    *,
    body: CancelTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: CancelTaskHarnAgentsProtocolVersion = CancelTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/tasks/{task_id}/cancel".format(
            task_id=quote(str(task_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ErrorResponse | Task:
    if response.status_code == 200:
        response_200 = Task.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | ErrorResponse | Task]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CancelTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: CancelTaskHarnAgentsProtocolVersion = CancelTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | ErrorResponse | Task]:
    """Request cooperative Task cancellation.

    Args:
        task_id (str):
        harn_agents_protocol_version (CancelTaskHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (CancelTaskRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ErrorResponse | Task]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CancelTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: CancelTaskHarnAgentsProtocolVersion = CancelTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Error | ErrorResponse | Task | None:
    """Request cooperative Task cancellation.

    Args:
        task_id (str):
        harn_agents_protocol_version (CancelTaskHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (CancelTaskRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ErrorResponse | Task
    """

    return sync_detailed(
        task_id=task_id,
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CancelTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: CancelTaskHarnAgentsProtocolVersion = CancelTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | ErrorResponse | Task]:
    """Request cooperative Task cancellation.

    Args:
        task_id (str):
        harn_agents_protocol_version (CancelTaskHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (CancelTaskRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ErrorResponse | Task]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CancelTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: CancelTaskHarnAgentsProtocolVersion = CancelTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Error | ErrorResponse | Task | None:
    """Request cooperative Task cancellation.

    Args:
        task_id (str):
        harn_agents_protocol_version (CancelTaskHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (CancelTaskRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ErrorResponse | Task
    """

    return (
        await asyncio_detailed(
            task_id=task_id,
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
