from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject


T = TypeVar("T", bound="A2AAgentCapabilities")


@_attrs_define
class A2AAgentCapabilities:
    """
    Attributes:
        streaming (bool | Unset):
        push_notifications (bool | Unset):
        extensions (list[JsonObject] | Unset):
        extended_agent_card (bool | Unset):
    """

    streaming: bool | Unset = UNSET
    push_notifications: bool | Unset = UNSET
    extensions: list[JsonObject] | Unset = UNSET
    extended_agent_card: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        streaming = self.streaming

        push_notifications = self.push_notifications

        extensions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.extensions, Unset):
            extensions = []
            for extensions_item_data in self.extensions:
                extensions_item = extensions_item_data.to_dict()
                extensions.append(extensions_item)

        extended_agent_card = self.extended_agent_card

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if streaming is not UNSET:
            field_dict["streaming"] = streaming
        if push_notifications is not UNSET:
            field_dict["pushNotifications"] = push_notifications
        if extensions is not UNSET:
            field_dict["extensions"] = extensions
        if extended_agent_card is not UNSET:
            field_dict["extendedAgentCard"] = extended_agent_card

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject

        d = dict(src_dict)
        streaming = d.pop("streaming", UNSET)

        push_notifications = d.pop("pushNotifications", UNSET)

        _extensions = d.pop("extensions", UNSET)
        extensions: list[JsonObject] | Unset = UNSET
        if _extensions is not UNSET:
            extensions = []
            for extensions_item_data in _extensions:
                extensions_item = JsonObject.from_dict(extensions_item_data)

                extensions.append(extensions_item)

        extended_agent_card = d.pop("extendedAgentCard", UNSET)

        a2a_agent_capabilities = cls(
            streaming=streaming,
            push_notifications=push_notifications,
            extensions=extensions,
            extended_agent_card=extended_agent_card,
        )

        a2a_agent_capabilities.additional_properties = d
        return a2a_agent_capabilities

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
