from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="UpdateWorkspaceRequest")


@_attrs_define
class UpdateWorkspaceRequest:
    """
    Attributes:
        name (str | Unset):
        capabilities (list[str] | Unset):
        quota_id (None | str | Unset):
        metadata (Metadata | Unset):
    """

    name: str | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    quota_id: None | str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        quota_id: None | str | Unset
        if isinstance(self.quota_id, Unset):
            quota_id = UNSET
        else:
            quota_id = self.quota_id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if quota_id is not UNSET:
            field_dict["quota_id"] = quota_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        def _parse_quota_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        quota_id = _parse_quota_id(d.pop("quota_id", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        update_workspace_request = cls(
            name=name,
            capabilities=capabilities,
            quota_id=quota_id,
            metadata=metadata,
        )

        update_workspace_request.additional_properties = d
        return update_workspace_request

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
