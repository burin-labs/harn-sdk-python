from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.discovery_current_version import DiscoveryCurrentVersion
from ..models.discovery_object import DiscoveryObject
from ..models.discovery_protocol_family import DiscoveryProtocolFamily

if TYPE_CHECKING:
    from ..models.discovery_capabilities import DiscoveryCapabilities


T = TypeVar("T", bound="Discovery")


@_attrs_define
class Discovery:
    """
    Attributes:
        object_ (DiscoveryObject):
        protocol_family (DiscoveryProtocolFamily):
        current_version (DiscoveryCurrentVersion):
        supported_versions (list[str]):
        capabilities (DiscoveryCapabilities):
    """

    object_: DiscoveryObject
    protocol_family: DiscoveryProtocolFamily
    current_version: DiscoveryCurrentVersion
    supported_versions: list[str]
    capabilities: DiscoveryCapabilities
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        protocol_family = self.protocol_family.value

        current_version = self.current_version.value

        supported_versions = self.supported_versions

        capabilities = self.capabilities.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "protocol_family": protocol_family,
                "current_version": current_version,
                "supported_versions": supported_versions,
                "capabilities": capabilities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.discovery_capabilities import DiscoveryCapabilities

        d = dict(src_dict)
        object_ = DiscoveryObject(d.pop("object"))

        protocol_family = DiscoveryProtocolFamily(d.pop("protocol_family"))

        current_version = DiscoveryCurrentVersion(d.pop("current_version"))

        supported_versions = cast(list[str], d.pop("supported_versions"))

        capabilities = DiscoveryCapabilities.from_dict(d.pop("capabilities"))

        discovery = cls(
            object_=object_,
            protocol_family=protocol_family,
            current_version=current_version,
            supported_versions=supported_versions,
            capabilities=capabilities,
        )

        discovery.additional_properties = d
        return discovery

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
