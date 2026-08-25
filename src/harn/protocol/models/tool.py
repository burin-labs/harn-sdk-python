from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.tool_object import ToolObject

if TYPE_CHECKING:
    from ..models.json_object import JsonObject


T = TypeVar("T", bound="Tool")


@_attrs_define
class Tool:
    """
    Attributes:
        id (str):
        object_ (ToolObject):
        name (str):
        description (str):
        input_schema (JsonObject):
        output_schema (JsonObject):
    """

    id: str
    object_: ToolObject
    name: str
    description: str
    input_schema: JsonObject
    output_schema: JsonObject
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        name = self.name

        description = self.description

        input_schema = self.input_schema.to_dict()

        output_schema = self.output_schema.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "name": name,
                "description": description,
                "input_schema": input_schema,
                "output_schema": output_schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject

        d = dict(src_dict)
        id = d.pop("id")

        object_ = ToolObject(d.pop("object"))

        name = d.pop("name")

        description = d.pop("description")

        input_schema = JsonObject.from_dict(d.pop("input_schema"))

        output_schema = JsonObject.from_dict(d.pop("output_schema"))

        tool = cls(
            id=id,
            object_=object_,
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
        )

        tool.additional_properties = d
        return tool

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
