from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.branch import Branch
from ...models.error_response import ErrorResponse
from ...models.get_branch_harn_agents_protocol_version import (
    GetBranchHarnAgentsProtocolVersion,
)
from ...types import Response


def _get_kwargs(
    branch_id: str,
    *,
    harn_agents_protocol_version: GetBranchHarnAgentsProtocolVersion = GetBranchHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/branches/{branch_id}".format(
            branch_id=quote(str(branch_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Branch | ErrorResponse:
    if response.status_code == 200:
        response_200 = Branch.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Branch | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    branch_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetBranchHarnAgentsProtocolVersion = GetBranchHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[Branch | ErrorResponse]:
    """Retrieve a Branch.

    Args:
        branch_id (str):
        harn_agents_protocol_version (GetBranchHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Branch | ErrorResponse]
    """

    kwargs = _get_kwargs(
        branch_id=branch_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    branch_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetBranchHarnAgentsProtocolVersion = GetBranchHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Branch | ErrorResponse | None:
    """Retrieve a Branch.

    Args:
        branch_id (str):
        harn_agents_protocol_version (GetBranchHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Branch | ErrorResponse
    """

    return sync_detailed(
        branch_id=branch_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    branch_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetBranchHarnAgentsProtocolVersion = GetBranchHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[Branch | ErrorResponse]:
    """Retrieve a Branch.

    Args:
        branch_id (str):
        harn_agents_protocol_version (GetBranchHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Branch | ErrorResponse]
    """

    kwargs = _get_kwargs(
        branch_id=branch_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    branch_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetBranchHarnAgentsProtocolVersion = GetBranchHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Branch | ErrorResponse | None:
    """Retrieve a Branch.

    Args:
        branch_id (str):
        harn_agents_protocol_version (GetBranchHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Branch | ErrorResponse
    """

    return (
        await asyncio_detailed(
            branch_id=branch_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
