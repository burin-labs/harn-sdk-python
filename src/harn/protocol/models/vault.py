from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.vault_object import VaultObject

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Vault")


@_attrs_define
class Vault:
    """
    Attributes:
        id (str):
        object_ (VaultObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        workspace_id (None | str):
        provider (str):
        capabilities (list[str]):
    """

    id: str
    object_: VaultObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    workspace_id: None | str
    provider: str
    capabilities: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        workspace_id: None | str
        workspace_id = self.workspace_id

        provider = self.provider

        capabilities = self.capabilities

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "workspace_id": workspace_id,
                "provider": provider,
                "capabilities": capabilities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = VaultObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        def _parse_workspace_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        workspace_id = _parse_workspace_id(d.pop("workspace_id"))

        provider = d.pop("provider")

        capabilities = cast(list[str], d.pop("capabilities"))

        vault = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            workspace_id=workspace_id,
            provider=provider,
            capabilities=capabilities,
        )

        vault.additional_properties = d
        return vault

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
