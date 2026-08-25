from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.image_ref_part_type import ImageRefPartType
from ..models.part_visibility import PartVisibility

T = TypeVar("T", bound="ImageRefPart")


@_attrs_define
class ImageRefPart:
    """
    Attributes:
        type_ (ImageRefPartType):
        artifact_id (str):
        mime_type (str):
        visibility (PartVisibility):
    """

    type_: ImageRefPartType
    artifact_id: str
    mime_type: str
    visibility: PartVisibility
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        artifact_id = self.artifact_id

        mime_type = self.mime_type

        visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "artifact_id": artifact_id,
                "mime_type": mime_type,
                "visibility": visibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = ImageRefPartType(d.pop("type"))

        artifact_id = d.pop("artifact_id")

        mime_type = d.pop("mime_type")

        visibility = PartVisibility(d.pop("visibility"))

        image_ref_part = cls(
            type_=type_,
            artifact_id=artifact_id,
            mime_type=mime_type,
            visibility=visibility,
        )

        image_ref_part.additional_properties = d
        return image_ref_part

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
