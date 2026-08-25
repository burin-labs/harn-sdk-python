from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.part_visibility import PartVisibility
from ..models.text_part_type import TextPartType

T = TypeVar("T", bound="TextPart")


@_attrs_define
class TextPart:
    """
    Attributes:
        type_ (TextPartType):
        text (str):
        visibility (PartVisibility):
    """

    type_: TextPartType
    text: str
    visibility: PartVisibility
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        text = self.text

        visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "text": text,
                "visibility": visibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = TextPartType(d.pop("type"))

        text = d.pop("text")

        visibility = PartVisibility(d.pop("visibility"))

        text_part = cls(
            type_=type_,
            text=text,
            visibility=visibility,
        )

        text_part.additional_properties = d
        return text_part

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
