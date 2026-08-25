from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.json_part_type import JsonPartType
from ..models.part_visibility import PartVisibility

T = TypeVar("T", bound="JsonPart")


@_attrs_define
class JsonPart:
    """
    Attributes:
        type_ (JsonPartType):
        value (Any): Any JSON value.
        visibility (PartVisibility):
    """

    type_: JsonPartType
    value: Any
    visibility: PartVisibility
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        value = self.value

        visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "value": value,
                "visibility": visibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = JsonPartType(d.pop("type"))

        value = d.pop("value")

        visibility = PartVisibility(d.pop("visibility"))

        json_part = cls(
            type_=type_,
            value=value,
            visibility=visibility,
        )

        json_part.additional_properties = d
        return json_part

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
