from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_vault_harn_agents_protocol_version import (
    GetVaultHarnAgentsProtocolVersion,
)
from ...models.vault import Vault
from ...types import Response


def _get_kwargs(
    vault_id: str,
    *,
    harn_agents_protocol_version: GetVaultHarnAgentsProtocolVersion = GetVaultHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/vaults/{vault_id}".format(
            vault_id=quote(str(vault_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Vault:
    if response.status_code == 200:
        response_200 = Vault.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Vault]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    vault_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetVaultHarnAgentsProtocolVersion = GetVaultHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Vault]:
    """Retrieve Vault metadata without secret values.

    Args:
        vault_id (str):
        harn_agents_protocol_version (GetVaultHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Vault]
    """

    kwargs = _get_kwargs(
        vault_id=vault_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    vault_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetVaultHarnAgentsProtocolVersion = GetVaultHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Vault | None:
    """Retrieve Vault metadata without secret values.

    Args:
        vault_id (str):
        harn_agents_protocol_version (GetVaultHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Vault
    """

    return sync_detailed(
        vault_id=vault_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    vault_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetVaultHarnAgentsProtocolVersion = GetVaultHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | Vault]:
    """Retrieve Vault metadata without secret values.

    Args:
        vault_id (str):
        harn_agents_protocol_version (GetVaultHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Vault]
    """

    kwargs = _get_kwargs(
        vault_id=vault_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    vault_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetVaultHarnAgentsProtocolVersion = GetVaultHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | Vault | None:
    """Retrieve Vault metadata without secret values.

    Args:
        vault_id (str):
        harn_agents_protocol_version (GetVaultHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Vault
    """

    return (
        await asyncio_detailed(
            vault_id=vault_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
