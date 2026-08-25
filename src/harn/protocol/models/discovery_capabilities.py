from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscoveryCapabilities")


@_attrs_define
class DiscoveryCapabilities:
    """
    Attributes:
        rest (bool | Unset):
        sse (bool | Unset):
        websocket (bool | Unset):
        receipts (bool | Unset):
        replay (bool | Unset):
    """

    rest: bool | Unset = UNSET
    sse: bool | Unset = UNSET
    websocket: bool | Unset = UNSET
    receipts: bool | Unset = UNSET
    replay: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rest = self.rest

        sse = self.sse

        websocket = self.websocket

        receipts = self.receipts

        replay = self.replay

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rest is not UNSET:
            field_dict["rest"] = rest
        if sse is not UNSET:
            field_dict["sse"] = sse
        if websocket is not UNSET:
            field_dict["websocket"] = websocket
        if receipts is not UNSET:
            field_dict["receipts"] = receipts
        if replay is not UNSET:
            field_dict["replay"] = replay

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        rest = d.pop("rest", UNSET)

        sse = d.pop("sse", UNSET)

        websocket = d.pop("websocket", UNSET)

        receipts = d.pop("receipts", UNSET)

        replay = d.pop("replay", UNSET)

        discovery_capabilities = cls(
            rest=rest,
            sse=sse,
            websocket=websocket,
            receipts=receipts,
            replay=replay,
        )

        discovery_capabilities.additional_properties = d
        return discovery_capabilities

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
