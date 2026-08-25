from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.revoke_permission_rule_harn_agents_protocol_version import (
    RevokePermissionRuleHarnAgentsProtocolVersion,
)
from ...types import Response


def _get_kwargs(
    rule_id: str,
    *,
    harn_agents_protocol_version: RevokePermissionRuleHarnAgentsProtocolVersion = RevokePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/permissions/rules/{rule_id}".format(
            rule_id=quote(str(rule_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ErrorResponse:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    rule_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: RevokePermissionRuleHarnAgentsProtocolVersion = RevokePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[Any | ErrorResponse]:
    r"""Soft-revoke a \"remember\" rule.

     Marks the rule as revoked. Subsequent evaluations skip it; the
    original row is preserved for audit. Use the audit API to find
    the original `created_at`/`created_by` after revocation.

    Args:
        rule_id (str):
        harn_agents_protocol_version (RevokePermissionRuleHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        rule_id=rule_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rule_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: RevokePermissionRuleHarnAgentsProtocolVersion = RevokePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Any | ErrorResponse | None:
    r"""Soft-revoke a \"remember\" rule.

     Marks the rule as revoked. Subsequent evaluations skip it; the
    original row is preserved for audit. Use the audit API to find
    the original `created_at`/`created_by` after revocation.

    Args:
        rule_id (str):
        harn_agents_protocol_version (RevokePermissionRuleHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return sync_detailed(
        rule_id=rule_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    rule_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: RevokePermissionRuleHarnAgentsProtocolVersion = RevokePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[Any | ErrorResponse]:
    r"""Soft-revoke a \"remember\" rule.

     Marks the rule as revoked. Subsequent evaluations skip it; the
    original row is preserved for audit. Use the audit API to find
    the original `created_at`/`created_by` after revocation.

    Args:
        rule_id (str):
        harn_agents_protocol_version (RevokePermissionRuleHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        rule_id=rule_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rule_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: RevokePermissionRuleHarnAgentsProtocolVersion = RevokePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Any | ErrorResponse | None:
    r"""Soft-revoke a \"remember\" rule.

     Marks the rule as revoked. Subsequent evaluations skip it; the
    original row is preserved for audit. Use the audit API to find
    the original `created_at`/`created_by` after revocation.

    Args:
        rule_id (str):
        harn_agents_protocol_version (RevokePermissionRuleHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            rule_id=rule_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
