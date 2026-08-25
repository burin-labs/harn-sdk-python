from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.capability_summary import CapabilitySummary
from ...models.error_response import ErrorResponse
from ...models.list_capabilities_harn_agents_protocol_version import (
    ListCapabilitiesHarnAgentsProtocolVersion,
)
from ...types import Response


def _get_kwargs(
    *,
    harn_agents_protocol_version: ListCapabilitiesHarnAgentsProtocolVersion = ListCapabilitiesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/capabilities",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CapabilitySummary | ErrorResponse:
    if response.status_code == 200:
        response_200 = CapabilitySummary.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CapabilitySummary | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: ListCapabilitiesHarnAgentsProtocolVersion = ListCapabilitiesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[CapabilitySummary | ErrorResponse]:
    """List local API capabilities.

    Args:
        harn_agents_protocol_version (ListCapabilitiesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CapabilitySummary | ErrorResponse]
    """

    kwargs = _get_kwargs(
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: ListCapabilitiesHarnAgentsProtocolVersion = ListCapabilitiesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> CapabilitySummary | ErrorResponse | None:
    """List local API capabilities.

    Args:
        harn_agents_protocol_version (ListCapabilitiesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilitySummary | ErrorResponse
    """

    return sync_detailed(
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: ListCapabilitiesHarnAgentsProtocolVersion = ListCapabilitiesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[CapabilitySummary | ErrorResponse]:
    """List local API capabilities.

    Args:
        harn_agents_protocol_version (ListCapabilitiesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CapabilitySummary | ErrorResponse]
    """

    kwargs = _get_kwargs(
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: ListCapabilitiesHarnAgentsProtocolVersion = ListCapabilitiesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> CapabilitySummary | ErrorResponse | None:
    """List local API capabilities.

    Args:
        harn_agents_protocol_version (ListCapabilitiesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilitySummary | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
