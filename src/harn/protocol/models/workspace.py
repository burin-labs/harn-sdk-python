from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.workspace_object import WorkspaceObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Workspace")


@_attrs_define
class Workspace:
    """
    Attributes:
        id (str):
        object_ (WorkspaceObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        name (str):
        root (str):
        default_branch_id (None | str):
        host (None | str | Unset):
        repository (None | str | Unset):
        tenant_id (None | str | Unset):
        capabilities (list[str] | Unset):
        connectors (list[str] | Unset):
        quota_id (None | str | Unset):
    """

    id: str
    object_: WorkspaceObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    name: str
    root: str
    default_branch_id: None | str
    host: None | str | Unset = UNSET
    repository: None | str | Unset = UNSET
    tenant_id: None | str | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    connectors: list[str] | Unset = UNSET
    quota_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        name = self.name

        root = self.root

        default_branch_id: None | str
        default_branch_id = self.default_branch_id

        host: None | str | Unset
        if isinstance(self.host, Unset):
            host = UNSET
        else:
            host = self.host

        repository: None | str | Unset
        if isinstance(self.repository, Unset):
            repository = UNSET
        else:
            repository = self.repository

        tenant_id: None | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        else:
            tenant_id = self.tenant_id

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        connectors: list[str] | Unset = UNSET
        if not isinstance(self.connectors, Unset):
            connectors = self.connectors

        quota_id: None | str | Unset
        if isinstance(self.quota_id, Unset):
            quota_id = UNSET
        else:
            quota_id = self.quota_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "name": name,
                "root": root,
                "default_branch_id": default_branch_id,
            }
        )
        if host is not UNSET:
            field_dict["host"] = host
        if repository is not UNSET:
            field_dict["repository"] = repository
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if connectors is not UNSET:
            field_dict["connectors"] = connectors
        if quota_id is not UNSET:
            field_dict["quota_id"] = quota_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = WorkspaceObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        name = d.pop("name")

        root = d.pop("root")

        def _parse_default_branch_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        default_branch_id = _parse_default_branch_id(d.pop("default_branch_id"))

        def _parse_host(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        host = _parse_host(d.pop("host", UNSET))

        def _parse_repository(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        repository = _parse_repository(d.pop("repository", UNSET))

        def _parse_tenant_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenant_id", UNSET))

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        connectors = cast(list[str], d.pop("connectors", UNSET))

        def _parse_quota_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        quota_id = _parse_quota_id(d.pop("quota_id", UNSET))

        workspace = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            name=name,
            root=root,
            default_branch_id=default_branch_id,
            host=host,
            repository=repository,
            tenant_id=tenant_id,
            capabilities=capabilities,
            connectors=connectors,
            quota_id=quota_id,
        )

        workspace.additional_properties = d
        return workspace

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
