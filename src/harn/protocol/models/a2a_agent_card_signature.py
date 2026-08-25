from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject


T = TypeVar("T", bound="A2AAgentCardSignature")


@_attrs_define
class A2AAgentCardSignature:
    """
    Attributes:
        protected (str):
        signature (str):
        header (JsonObject | Unset):
    """

    protected: str
    signature: str
    header: JsonObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        protected = self.protected

        signature = self.signature

        header: dict[str, Any] | Unset = UNSET
        if not isinstance(self.header, Unset):
            header = self.header.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "protected": protected,
                "signature": signature,
            }
        )
        if header is not UNSET:
            field_dict["header"] = header

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject

        d = dict(src_dict)
        protected = d.pop("protected")

        signature = d.pop("signature")

        _header = d.pop("header", UNSET)
        header: JsonObject | Unset
        if isinstance(_header, Unset):
            header = UNSET
        else:
            header = JsonObject.from_dict(_header)

        a2a_agent_card_signature = cls(
            protected=protected,
            signature=signature,
            header=header,
        )

        a2a_agent_card_signature.additional_properties = d
        return a2a_agent_card_signature

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
