from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.replay_task_harn_agents_protocol_version import (
    ReplayTaskHarnAgentsProtocolVersion,
)
from ...models.replay_task_request import ReplayTaskRequest
from ...models.task import Task
from ...types import UNSET, Response, Unset


def _get_kwargs(
    task_id: str,
    *,
    body: ReplayTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: ReplayTaskHarnAgentsProtocolVersion = ReplayTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/tasks/{task_id}/replay".format(
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
) -> ErrorResponse | Task:
    if response.status_code == 202:
        response_202 = Task.from_dict(response.json())

        return response_202

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Task]:
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
    body: ReplayTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: ReplayTaskHarnAgentsProtocolVersion = ReplayTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Task]:
    """Replay a Task from its durable EventLog.

     Creates a new Task by replaying the original Task's durable event log.
    The returned Task is the replay Task and MUST set `parent_task_id` to
    the source Task id. Overrides substitute recorded nondeterministic
    dependencies such as LLM responses, MCP tool returns, secret values,
    clock reads, and host facts; every applied substitution MUST be
    represented as a replay Receipt delta.

    Args:
        task_id (str):
        harn_agents_protocol_version (ReplayTaskHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (ReplayTaskRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Task]
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
    body: ReplayTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: ReplayTaskHarnAgentsProtocolVersion = ReplayTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Task | None:
    """Replay a Task from its durable EventLog.

     Creates a new Task by replaying the original Task's durable event log.
    The returned Task is the replay Task and MUST set `parent_task_id` to
    the source Task id. Overrides substitute recorded nondeterministic
    dependencies such as LLM responses, MCP tool returns, secret values,
    clock reads, and host facts; every applied substitution MUST be
    represented as a replay Receipt delta.

    Args:
        task_id (str):
        harn_agents_protocol_version (ReplayTaskHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (ReplayTaskRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Task
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
    body: ReplayTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: ReplayTaskHarnAgentsProtocolVersion = ReplayTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Task]:
    """Replay a Task from its durable EventLog.

     Creates a new Task by replaying the original Task's durable event log.
    The returned Task is the replay Task and MUST set `parent_task_id` to
    the source Task id. Overrides substitute recorded nondeterministic
    dependencies such as LLM responses, MCP tool returns, secret values,
    clock reads, and host facts; every applied substitution MUST be
    represented as a replay Receipt delta.

    Args:
        task_id (str):
        harn_agents_protocol_version (ReplayTaskHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (ReplayTaskRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Task]
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
    body: ReplayTaskRequest | Unset = UNSET,
    harn_agents_protocol_version: ReplayTaskHarnAgentsProtocolVersion = ReplayTaskHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Task | None:
    """Replay a Task from its durable EventLog.

     Creates a new Task by replaying the original Task's durable event log.
    The returned Task is the replay Task and MUST set `parent_task_id` to
    the source Task id. Overrides substitute recorded nondeterministic
    dependencies such as LLM responses, MCP tool returns, secret values,
    clock reads, and host facts; every applied substitution MUST be
    represented as a replay Receipt delta.

    Args:
        task_id (str):
        harn_agents_protocol_version (ReplayTaskHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (ReplayTaskRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Task
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
