from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.capability_summary_object import CapabilitySummaryObject

if TYPE_CHECKING:
    from ..models.capability import Capability


T = TypeVar("T", bound="CapabilitySummary")


@_attrs_define
class CapabilitySummary:
    """
    Attributes:
        object_ (CapabilitySummaryObject):
        capabilities (list[Capability]):
    """

    object_: CapabilitySummaryObject
    capabilities: list[Capability]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        capabilities = []
        for capabilities_item_data in self.capabilities:
            capabilities_item = capabilities_item_data.to_dict()
            capabilities.append(capabilities_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "capabilities": capabilities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.capability import Capability

        d = dict(src_dict)
        object_ = CapabilitySummaryObject(d.pop("object"))

        capabilities = []
        _capabilities = d.pop("capabilities")
        for capabilities_item_data in _capabilities:
            capabilities_item = Capability.from_dict(capabilities_item_data)

            capabilities.append(capabilities_item)

        capability_summary = cls(
            object_=object_,
            capabilities=capabilities,
        )

        capability_summary.additional_properties = d
        return capability_summary

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
