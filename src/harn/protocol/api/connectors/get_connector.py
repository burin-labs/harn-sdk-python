from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.connector import Connector
from ...models.error_response import ErrorResponse
from ...models.get_connector_harn_agents_protocol_version import (
    GetConnectorHarnAgentsProtocolVersion,
)
from ...types import Response


def _get_kwargs(
    connector_id: str,
    *,
    harn_agents_protocol_version: GetConnectorHarnAgentsProtocolVersion = GetConnectorHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/connectors/{connector_id}".format(
            connector_id=quote(str(connector_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Connector | ErrorResponse:
    if response.status_code == 200:
        response_200 = Connector.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Connector | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    connector_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetConnectorHarnAgentsProtocolVersion = GetConnectorHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[Connector | ErrorResponse]:
    """Retrieve a Connector.

    Args:
        connector_id (str):
        harn_agents_protocol_version (GetConnectorHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Connector | ErrorResponse]
    """

    kwargs = _get_kwargs(
        connector_id=connector_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    connector_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetConnectorHarnAgentsProtocolVersion = GetConnectorHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Connector | ErrorResponse | None:
    """Retrieve a Connector.

    Args:
        connector_id (str):
        harn_agents_protocol_version (GetConnectorHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Connector | ErrorResponse
    """

    return sync_detailed(
        connector_id=connector_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    connector_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetConnectorHarnAgentsProtocolVersion = GetConnectorHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[Connector | ErrorResponse]:
    """Retrieve a Connector.

    Args:
        connector_id (str):
        harn_agents_protocol_version (GetConnectorHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Connector | ErrorResponse]
    """

    kwargs = _get_kwargs(
        connector_id=connector_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    connector_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetConnectorHarnAgentsProtocolVersion = GetConnectorHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Connector | ErrorResponse | None:
    """Retrieve a Connector.

    Args:
        connector_id (str):
        harn_agents_protocol_version (GetConnectorHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Connector | ErrorResponse
    """

    return (
        await asyncio_detailed(
            connector_id=connector_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
