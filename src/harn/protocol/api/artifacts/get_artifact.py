from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.artifact import Artifact
from ...models.error_response import ErrorResponse
from ...models.get_artifact_harn_agents_protocol_version import (
    GetArtifactHarnAgentsProtocolVersion,
)
from ...types import Response


def _get_kwargs(
    artifact_id: str,
    *,
    harn_agents_protocol_version: GetArtifactHarnAgentsProtocolVersion = GetArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Harn-Agents-Protocol-Version"] = str(harn_agents_protocol_version)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/artifacts/{artifact_id}".format(
            artifact_id=quote(str(artifact_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Artifact | ErrorResponse:
    if response.status_code == 200:
        response_200 = Artifact.from_dict(response.json())

        return response_200

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
    artifact_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetArtifactHarnAgentsProtocolVersion = GetArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[Artifact | ErrorResponse]:
    """Retrieve Artifact metadata.

    Args:
        artifact_id (str):
        harn_agents_protocol_version (GetArtifactHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Artifact | ErrorResponse]
    """

    kwargs = _get_kwargs(
        artifact_id=artifact_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    artifact_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetArtifactHarnAgentsProtocolVersion = GetArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Artifact | ErrorResponse | None:
    """Retrieve Artifact metadata.

    Args:
        artifact_id (str):
        harn_agents_protocol_version (GetArtifactHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Artifact | ErrorResponse
    """

    return sync_detailed(
        artifact_id=artifact_id,
        client=client,
        harn_agents_protocol_version=harn_agents_protocol_version,
    ).parsed


async def asyncio_detailed(
    artifact_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetArtifactHarnAgentsProtocolVersion = GetArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Response[Artifact | ErrorResponse]:
    """Retrieve Artifact metadata.

    Args:
        artifact_id (str):
        harn_agents_protocol_version (GetArtifactHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Artifact | ErrorResponse]
    """

    kwargs = _get_kwargs(
        artifact_id=artifact_id,
        harn_agents_protocol_version=harn_agents_protocol_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    artifact_id: str,
    *,
    client: AuthenticatedClient | Client,
    harn_agents_protocol_version: GetArtifactHarnAgentsProtocolVersion = GetArtifactHarnAgentsProtocolVersion.AGENTS_PROTOCOL_2026_04_25,
) -> Artifact | ErrorResponse | None:
    """Retrieve Artifact metadata.

    Args:
        artifact_id (str):
        harn_agents_protocol_version (GetArtifactHarnAgentsProtocolVersion):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Artifact | ErrorResponse
    """

    return (
        await asyncio_detailed(
            artifact_id=artifact_id,
            client=client,
            harn_agents_protocol_version=harn_agents_protocol_version,
        )
    ).parsed
