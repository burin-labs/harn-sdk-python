from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.part_visibility import PartVisibility
from ..models.tool_call_part_type import ToolCallPartType

if TYPE_CHECKING:
    from ..models.json_object import JsonObject


T = TypeVar("T", bound="ToolCallPart")


@_attrs_define
class ToolCallPart:
    """
    Attributes:
        type_ (ToolCallPartType):
        tool_call_id (str):
        name (str):
        input_ (JsonObject):
        visibility (PartVisibility):
    """

    type_: ToolCallPartType
    tool_call_id: str
    name: str
    input_: JsonObject
    visibility: PartVisibility
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        tool_call_id = self.tool_call_id

        name = self.name

        input_ = self.input_.to_dict()

        visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "tool_call_id": tool_call_id,
                "name": name,
                "input": input_,
                "visibility": visibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject

        d = dict(src_dict)
        type_ = ToolCallPartType(d.pop("type"))

        tool_call_id = d.pop("tool_call_id")

        name = d.pop("name")

        input_ = JsonObject.from_dict(d.pop("input"))

        visibility = PartVisibility(d.pop("visibility"))

        tool_call_part = cls(
            type_=type_,
            tool_call_id=tool_call_id,
            name=name,
            input_=input_,
            visibility=visibility,
        )

        tool_call_part.additional_properties = d
        return tool_call_part

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
