from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.create_memory_request_scope import CreateMemoryRequestScope
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject
    from ..models.metadata import Metadata


T = TypeVar("T", bound="CreateMemoryRequest")


@_attrs_define
class CreateMemoryRequest:
    """
    Attributes:
        scope (CreateMemoryRequestScope):
        owner_id (str):
        content (Any): Any JSON value.
        provenance (JsonObject):
        metadata (Metadata | Unset):
    """

    scope: CreateMemoryRequestScope
    owner_id: str
    content: Any
    provenance: JsonObject
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope.value

        owner_id = self.owner_id

        content = self.content

        provenance = self.provenance.to_dict()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope": scope,
                "owner_id": owner_id,
                "content": content,
                "provenance": provenance,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject
        from ..models.metadata import Metadata

        d = dict(src_dict)
        scope = CreateMemoryRequestScope(d.pop("scope"))

        owner_id = d.pop("owner_id")

        content = d.pop("content")

        provenance = JsonObject.from_dict(d.pop("provenance"))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        create_memory_request = cls(
            scope=scope,
            owner_id=owner_id,
            content=content,
            provenance=provenance,
            metadata=metadata,
        )

        create_memory_request.additional_properties = d
        return create_memory_request

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
