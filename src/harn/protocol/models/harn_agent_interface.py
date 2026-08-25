from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.harn_agent_interface_transport import HarnAgentInterfaceTransport

T = TypeVar("T", bound="HarnAgentInterface")


@_attrs_define
class HarnAgentInterface:
    """
    Attributes:
        transport (HarnAgentInterfaceTransport):
        url (str):
    """

    transport: HarnAgentInterfaceTransport
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transport = self.transport.value

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transport": transport,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        transport = HarnAgentInterfaceTransport(d.pop("transport"))

        url = d.pop("url")

        harn_agent_interface = cls(
            transport=transport,
            url=url,
        )

        harn_agent_interface.additional_properties = d
        return harn_agent_interface

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
