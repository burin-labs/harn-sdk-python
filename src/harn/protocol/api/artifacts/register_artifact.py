from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.artifact import Artifact
from ...models.error_response import ErrorResponse
from ...models.register_artifact_harn_agents_protocol_version import (
    RegisterArtifactHarnAgentsProtocolVersion,
)
from ...models.register_artifact_request import RegisterArtifactRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: RegisterArtifactRequest,
    harn_agents_protocol_version: RegisterArtifactHarnAgentsProtocolVersion = RegisterArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/artifacts",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Artifact | ErrorResponse:
    if response.status_code == 201:
        response_201 = Artifact.from_dict(response.json())

        return response_201

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Artifact | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterArtifactRequest,
    harn_agents_protocol_version: RegisterArtifactHarnAgentsProtocolVersion = RegisterArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[Artifact | ErrorResponse]:
    """Register an Artifact or mediated upload URI.

    Args:
        harn_agents_protocol_version (RegisterArtifactHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (RegisterArtifactRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Artifact | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterArtifactRequest,
    harn_agents_protocol_version: RegisterArtifactHarnAgentsProtocolVersion = RegisterArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Artifact | ErrorResponse | None:
    """Register an Artifact or mediated upload URI.

    Args:
        harn_agents_protocol_version (RegisterArtifactHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (RegisterArtifactRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Artifact | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterArtifactRequest,
    harn_agents_protocol_version: RegisterArtifactHarnAgentsProtocolVersion = RegisterArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Response[Artifact | ErrorResponse]:
    """Register an Artifact or mediated upload URI.

    Args:
        harn_agents_protocol_version (RegisterArtifactHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (RegisterArtifactRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Artifact | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        harn_agents_protocol_version=harn_agents_protocol_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterArtifactRequest,
    harn_agents_protocol_version: RegisterArtifactHarnAgentsProtocolVersion = RegisterArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
    idempotency_key: str | Unset = UNSET,
) -> Artifact | ErrorResponse | None:
    """Register an Artifact or mediated upload URI.

    Args:
        harn_agents_protocol_version (RegisterArtifactHarnAgentsProtocolVersion):
        idempotency_key (str | Unset):
        body (RegisterArtifactRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Artifact | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            harn_agents_protocol_version=harn_agents_protocol_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
