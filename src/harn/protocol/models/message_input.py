from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.message_input_role import MessageInputRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_ref_part import ArtifactRefPart
    from ..models.file_ref_part import FileRefPart
    from ..models.image_ref_part import ImageRefPart
    from ..models.json_part import JsonPart
    from ..models.metadata import Metadata
    from ..models.text_part import TextPart
    from ..models.tool_call_part import ToolCallPart
    from ..models.tool_result_part import ToolResultPart


T = TypeVar("T", bound="MessageInput")


@_attrs_define
class MessageInput:
    """
    Attributes:
        role (MessageInputRole):
        parts (list[ArtifactRefPart | FileRefPart | ImageRefPart | JsonPart | TextPart | ToolCallPart |
            ToolResultPart]):
        metadata (Metadata | Unset):
    """

    role: MessageInputRole
    parts: list[
        ArtifactRefPart
        | FileRefPart
        | ImageRefPart
        | JsonPart
        | TextPart
        | ToolCallPart
        | ToolResultPart
    ]
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.artifact_ref_part import ArtifactRefPart
        from ..models.file_ref_part import FileRefPart
        from ..models.json_part import JsonPart
        from ..models.text_part import TextPart
        from ..models.tool_call_part import ToolCallPart
        from ..models.tool_result_part import ToolResultPart

        role = self.role.value

        parts = []
        for parts_item_data in self.parts:
            parts_item: dict[str, Any]
            if (
                isinstance(parts_item_data, TextPart)
                or isinstance(parts_item_data, JsonPart)
                or isinstance(parts_item_data, ToolCallPart)
                or isinstance(parts_item_data, ToolResultPart)
                or isinstance(parts_item_data, ArtifactRefPart)
                or isinstance(parts_item_data, FileRefPart)
            ):
                parts_item = parts_item_data.to_dict()
            else:
                parts_item = parts_item_data.to_dict()

            parts.append(parts_item)

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "parts": parts,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.artifact_ref_part import ArtifactRefPart
        from ..models.file_ref_part import FileRefPart
        from ..models.image_ref_part import ImageRefPart
        from ..models.json_part import JsonPart
        from ..models.metadata import Metadata
        from ..models.text_part import TextPart
        from ..models.tool_call_part import ToolCallPart
        from ..models.tool_result_part import ToolResultPart

        d = dict(src_dict)
        role = MessageInputRole(d.pop("role"))

        parts = []
        _parts = d.pop("parts")
        for parts_item_data in _parts:

            def _parse_parts_item(
                data: object,
            ) -> (
                ArtifactRefPart
                | FileRefPart
                | ImageRefPart
                | JsonPart
                | TextPart
                | ToolCallPart
                | ToolResultPart
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_input_type_0 = TextPart.from_dict(data)

                    return componentsschemas_part_input_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_input_type_1 = JsonPart.from_dict(data)

                    return componentsschemas_part_input_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_input_type_2 = ToolCallPart.from_dict(data)

                    return componentsschemas_part_input_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_input_type_3 = ToolResultPart.from_dict(data)

                    return componentsschemas_part_input_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_input_type_4 = ArtifactRefPart.from_dict(
                        data
                    )

                    return componentsschemas_part_input_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_input_type_5 = FileRefPart.from_dict(data)

                    return componentsschemas_part_input_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_part_input_type_6 = ImageRefPart.from_dict(data)

                return componentsschemas_part_input_type_6

            parts_item = _parse_parts_item(parts_item_data)

            parts.append(parts_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        message_input = cls(
            role=role,
            parts=parts,
            metadata=metadata,
        )

        message_input.additional_properties = d
        return message_input

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
