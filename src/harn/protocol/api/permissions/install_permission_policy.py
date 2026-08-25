from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.install_permission_policy_harn_agents_protocol_version import (
    InstallPermissionPolicyHarnAgentsProtocolVersion,
)
from ...models.permission_policy import PermissionPolicy
from ...models.permission_policy_response import PermissionPolicyResponse
from ...types import Response


def _get_kwargs(
    *,
    body: PermissionPolicy,
    harn_agents_protocol_version: InstallPermissionPolicyHarnAgentsProtocolVersion = InstallPermissionPolicyHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/permissions/policy",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | PermissionPolicyResponse:
    if response.status_code == 200:
        response_200 = PermissionPolicyResponse.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | PermissionPolicyResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PermissionPolicy,
    harn_agents_protocol_version: InstallPermissionPolicyHarnAgentsProtocolVersion = InstallPermissionPolicyHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | PermissionPolicyResponse]:
    """Replace the active permission policy.

     Validates the supplied policy (rejects empty patterns and invalid
    globs at parse time) and installs it. The previous version is
    replaced atomically; in-flight requests evaluated against the
    old version remain unaffected.

    Args:
        harn_agents_protocol_version (InstallPermissionPolicyHarnAgentsProtocolVersion):
        body (PermissionPolicy): Declared permission policy: read/write/exec globs, net host
            allowlist, llm provider list + optional cost ceiling,
            redaction patterns, escalation chain.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PermissionPolicyResponse]
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
    body: PermissionPolicy,
    harn_agents_protocol_version: InstallPermissionPolicyHarnAgentsProtocolVersion = InstallPermissionPolicyHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | PermissionPolicyResponse | None:
    """Replace the active permission policy.

     Validates the supplied policy (rejects empty patterns and invalid
    globs at parse time) and installs it. The previous version is
    replaced atomically; in-flight requests evaluated against the
    old version remain unaffected.

    Args:
        harn_agents_protocol_version (InstallPermissionPolicyHarnAgentsProtocolVersion):
        body (PermissionPolicy): Declared permission policy: read/write/exec globs, net host
            allowlist, llm provider list + optional cost ceiling,
            redaction patterns, escalation chain.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PermissionPolicyResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PermissionPolicy,
    harn_agents_protocol_version: InstallPermissionPolicyHarnAgentsProtocolVersion = InstallPermissionPolicyHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[ErrorResponse | PermissionPolicyResponse]:
    """Replace the active permission policy.

     Validates the supplied policy (rejects empty patterns and invalid
    globs at parse time) and installs it. The previous version is
    replaced atomically; in-flight requests evaluated against the
    old version remain unaffected.

    Args:
        harn_agents_protocol_version (InstallPermissionPolicyHarnAgentsProtocolVersion):
        body (PermissionPolicy): Declared permission policy: read/write/exec globs, net host
            allowlist, llm provider list + optional cost ceiling,
            redaction patterns, escalation chain.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PermissionPolicyResponse]
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
    body: PermissionPolicy,
    harn_agents_protocol_version: InstallPermissionPolicyHarnAgentsProtocolVersion = InstallPermissionPolicyHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> ErrorResponse | PermissionPolicyResponse | None:
    """Replace the active permission policy.

     Validates the supplied policy (rejects empty patterns and invalid
    globs at parse time) and installs it. The previous version is
    replaced atomically; in-flight requests evaluated against the
    old version remain unaffected.

    Args:
        harn_agents_protocol_version (InstallPermissionPolicyHarnAgentsProtocolVersion):
        body (PermissionPolicy): Declared permission policy: read/write/exec globs, net host
            allowlist, llm provider list + optional cost ceiling,
            redaction patterns, escalation chain.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PermissionPolicyResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
