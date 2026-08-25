from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_tool_harn_agents_protocol_version import (
    GetToolHarnAgentsProtocolVersion,
)
from ...models.tool import Tool
from ...types import Response


def _get_kwargs(
    tool_id: str,
    *,
    harn_agents_protocol_version: GetToolHarnAgentsProtocolVersion = GetToolHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tools/{tool_id}".format(
            tool_id=quote(str(tool_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Tool:
    if response.status_code == 200:
        response_200 = Tool.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Tool]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tool_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetToolHarnAgentsProtocolVersion = GetToolHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Tool]:
    """Retrieve a local control-plane tool description.

    Args:
        tool_id (str):
        harn_agents_protocol_version (GetToolHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Tool]
    """

    kwargs = _get_kwargs(
        tool_id=tool_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tool_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetToolHarnAgentsProtocolVersion = GetToolHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Tool | None:
    """Retrieve a local control-plane tool description.

    Args:
        tool_id (str):
        harn_agents_protocol_version (GetToolHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Tool
    """

    return sync_detailed(
        tool_id=tool_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    tool_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetToolHarnAgentsProtocolVersion = GetToolHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Tool]:
    """Retrieve a local control-plane tool description.

    Args:
        tool_id (str):
        harn_agents_protocol_version (GetToolHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Tool]
    """

    kwargs = _get_kwargs(
        tool_id=tool_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tool_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetToolHarnAgentsProtocolVersion = GetToolHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Tool | None:
    """Retrieve a local control-plane tool description.

    Args:
        tool_id (str):
        harn_agents_protocol_version (GetToolHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Tool
    """

    return (
        await asyncio_detailed(
            tool_id=tool_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
