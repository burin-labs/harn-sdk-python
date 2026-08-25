from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="A2AAgentInterface")


@_attrs_define
class A2AAgentInterface:
    """
    Attributes:
        url (str):
        protocol_binding (str):
        protocol_version (str):
        tenant (None | str | Unset):
    """

    url: str
    protocol_binding: str
    protocol_version: str
    tenant: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        protocol_binding = self.protocol_binding

        protocol_version = self.protocol_version

        tenant: None | str | Unset
        if isinstance(self.tenant, Unset):
            tenant = UNSET
        else:
            tenant = self.tenant

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "protocolBinding": protocol_binding,
                "protocolVersion": protocol_version,
            }
        )
        if tenant is not UNSET:
            field_dict["tenant"] = tenant

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        url = d.pop("url")

        protocol_binding = d.pop("protocolBinding")

        protocol_version = d.pop("protocolVersion")

        def _parse_tenant(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tenant = _parse_tenant(d.pop("tenant", UNSET))

        a2a_agent_interface = cls(
            url=url,
            protocol_binding=protocol_binding,
            protocol_version=protocol_version,
            tenant=tenant,
        )

        a2a_agent_interface.additional_properties = d
        return a2a_agent_interface

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
