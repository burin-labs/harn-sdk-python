from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.append_task_message_harn_agents_protocol_version import (
    AppendTaskMessageHarnAgentsProtocolVersion,
)
from ...models.append_task_message_request import AppendTaskMessageRequest
from ...models.error_response import ErrorResponse
from ...models.message import Message
from ...types import UNSET, Response, Unset


def _get_kwargs(
    task_id: str,
    *,
    body: AppendTaskMessageRequest,
    harn_agents_protocol_version: AppendTaskMessageHarnAgentsProtocolVersion = AppendTaskMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/tasks/{task_id}/messages".format(
            task_id=quote(str(task_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Message:
    if response.status_code == 201:
        response_201 = Message.from_dict(response.json())

        return response_201

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Message]:
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
    body: AppendTaskMessageRequest,
    harn_agents_protocol_version: AppendTaskMessageHarnAgentsProtocolVersion = AppendTaskMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Message]:
    """Steer a running Task with additional user input.

     Routes text through Harn's canonical active-prompt injection seam. Use
    the Task cancel endpoint for cancellation and the permission-response
    endpoint for tool confirmations; those controls retain their own typed
    audit contracts rather than being encoded as messages.

    Args:
        task_id (str):
        harn_agents_protocol_version (AppendTaskMessageHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (AppendTaskMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Message]
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
    body: AppendTaskMessageRequest,
    harn_agents_protocol_version: AppendTaskMessageHarnAgentsProtocolVersion = AppendTaskMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Message | None:
    """Steer a running Task with additional user input.

     Routes text through Harn's canonical active-prompt injection seam. Use
    the Task cancel endpoint for cancellation and the permission-response
    endpoint for tool confirmations; those controls retain their own typed
    audit contracts rather than being encoded as messages.

    Args:
        task_id (str):
        harn_agents_protocol_version (AppendTaskMessageHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (AppendTaskMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Message
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
    body: AppendTaskMessageRequest,
    harn_agents_protocol_version: AppendTaskMessageHarnAgentsProtocolVersion = AppendTaskMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Message]:
    """Steer a running Task with additional user input.

     Routes text through Harn's canonical active-prompt injection seam. Use
    the Task cancel endpoint for cancellation and the permission-response
    endpoint for tool confirmations; those controls retain their own typed
    audit contracts rather than being encoded as messages.

    Args:
        task_id (str):
        harn_agents_protocol_version (AppendTaskMessageHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (AppendTaskMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Message]
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
    body: AppendTaskMessageRequest,
    harn_agents_protocol_version: AppendTaskMessageHarnAgentsProtocolVersion = AppendTaskMessageHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Message | None:
    """Steer a running Task with additional user input.

     Routes text through Harn's canonical active-prompt injection seam. Use
    the Task cancel endpoint for cancellation and the permission-response
    endpoint for tool confirmations; those controls retain their own typed
    audit contracts rather than being encoded as messages.

    Args:
        task_id (str):
        harn_agents_protocol_version (AppendTaskMessageHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (AppendTaskMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Message
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
