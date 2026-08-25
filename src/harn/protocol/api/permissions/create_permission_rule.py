from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.create_permission_rule_harn_agents_protocol_version import (
    CreatePermissionRuleHarnAgentsProtocolVersion,
)
from ...models.error_response import ErrorResponse
from ...models.remember_rule import RememberRule
from ...types import Response


def _get_kwargs(
    *,
    body: RememberRule,
    harn_agents_protocol_version: CreatePermissionRuleHarnAgentsProtocolVersion = CreatePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/permissions/rules",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | RememberRule:
    if response.status_code == 200:
        response_200 = RememberRule.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | RememberRule]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RememberRule,
    harn_agents_protocol_version: CreatePermissionRuleHarnAgentsProtocolVersion = CreatePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | RememberRule]:
    r"""Install a new \"remember\" rule.

     Materializes a persistent rule that pins one action+target
    glob to a verdict at the chosen scope. Use the
    `respond_permission_request` endpoint with `remember: true`
    for the in-flight equivalent.

    Args:
        harn_agents_protocol_version (CreatePermissionRuleHarnAgentsProtocolVersion):
        body (RememberRule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | RememberRule]
    """

    kwargs = _get_kwargs(
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: RememberRule,
    harn_agents_protocol_version: CreatePermissionRuleHarnAgentsProtocolVersion = CreatePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | RememberRule | None:
    r"""Install a new \"remember\" rule.

     Materializes a persistent rule that pins one action+target
    glob to a verdict at the chosen scope. Use the
    `respond_permission_request` endpoint with `remember: true`
    for the in-flight equivalent.

    Args:
        harn_agents_protocol_version (CreatePermissionRuleHarnAgentsProtocolVersion):
        body (RememberRule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | RememberRule
    """

    return sync_detailed(
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RememberRule,
    harn_agents_protocol_version: CreatePermissionRuleHarnAgentsProtocolVersion = CreatePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | RememberRule]:
    r"""Install a new \"remember\" rule.

     Materializes a persistent rule that pins one action+target
    glob to a verdict at the chosen scope. Use the
    `respond_permission_request` endpoint with `remember: true`
    for the in-flight equivalent.

    Args:
        harn_agents_protocol_version (CreatePermissionRuleHarnAgentsProtocolVersion):
        body (RememberRule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | RememberRule]
    """

    kwargs = _get_kwargs(
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: RememberRule,
    harn_agents_protocol_version: CreatePermissionRuleHarnAgentsProtocolVersion = CreatePermissionRuleHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | RememberRule | None:
    r"""Install a new \"remember\" rule.

     Materializes a persistent rule that pins one action+target
    glob to a verdict at the chosen scope. Use the
    `respond_permission_request` endpoint with `remember: true`
    for the in-flight equivalent.

    Args:
        harn_agents_protocol_version (CreatePermissionRuleHarnAgentsProtocolVersion):
        body (RememberRule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | RememberRule
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
