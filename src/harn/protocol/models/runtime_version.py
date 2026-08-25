from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.runtime_version_object import RuntimeVersionObject

T = TypeVar("T", bound="RuntimeVersion")


@_attrs_define
class RuntimeVersion:
    """
    Attributes:
        object_ (RuntimeVersionObject):
        version (str):
        protocol_version (str):
    """

    object_: RuntimeVersionObject
    version: str
    protocol_version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        version = self.version

        protocol_version = self.protocol_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "version": version,
                "protocol_version": protocol_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        object_ = RuntimeVersionObject(d.pop("object"))

        version = d.pop("version")

        protocol_version = d.pop("protocol_version")

        runtime_version = cls(
            object_=object_,
            version=version,
            protocol_version=protocol_version,
        )

        runtime_version.additional_properties = d
        return runtime_version

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
