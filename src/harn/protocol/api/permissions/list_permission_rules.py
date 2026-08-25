from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_permission_rules_harn_agents_protocol_version import (
    ListPermissionRulesHarnAgentsProtocolVersion,
)
from ...models.remember_rule_list import RememberRuleList
from ...types import Response


def _get_kwargs(
    *,
    harn_agents_protocol_version: ListPermissionRulesHarnAgentsProtocolVersion = ListPermissionRulesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/permissions/rules",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | RememberRuleList:
    if response.status_code == 200:
        response_200 = RememberRuleList.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | RememberRuleList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: ListPermissionRulesHarnAgentsProtocolVersion = ListPermissionRulesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | RememberRuleList]:
    r"""List active \"remember\" rules.

     Returns every non-revoked, non-expired rule the store knows about,
    ordered narrowest-scope-first.

    Args:
        harn_agents_protocol_version (ListPermissionRulesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | RememberRuleList]
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
    harn_agents_protocol_version: ListPermissionRulesHarnAgentsProtocolVersion = ListPermissionRulesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | RememberRuleList | None:
    r"""List active \"remember\" rules.

     Returns every non-revoked, non-expired rule the store knows about,
    ordered narrowest-scope-first.

    Args:
        harn_agents_protocol_version (ListPermissionRulesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | RememberRuleList
    """

    return sync_detailed(
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: ListPermissionRulesHarnAgentsProtocolVersion = ListPermissionRulesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | RememberRuleList]:
    r"""List active \"remember\" rules.

     Returns every non-revoked, non-expired rule the store knows about,
    ordered narrowest-scope-first.

    Args:
        harn_agents_protocol_version (ListPermissionRulesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | RememberRuleList]
    """

    kwargs = _get_kwargs(
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: ListPermissionRulesHarnAgentsProtocolVersion = ListPermissionRulesHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | RememberRuleList | None:
    r"""List active \"remember\" rules.

     Returns every non-revoked, non-expired rule the store knows about,
    ordered narrowest-scope-first.

    Args:
        harn_agents_protocol_version (ListPermissionRulesHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | RememberRuleList
    """

    return (
        await asyncio_detailed(
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
