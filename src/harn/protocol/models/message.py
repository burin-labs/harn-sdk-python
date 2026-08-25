from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.message_object import MessageObject
from ..models.message_role import MessageRole
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


T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """
    Attributes:
        id (str):
        object_ (MessageObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        role (MessageRole):
        parts (list[ArtifactRefPart | FileRefPart | ImageRefPart | JsonPart | TextPart | ToolCallPart |
            ToolResultPart]):
        session_id (None | str | Unset):
        task_id (None | str | Unset):
    """

    id: str
    object_: MessageObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    role: MessageRole
    parts: list[
        ArtifactRefPart
        | FileRefPart
        | ImageRefPart
        | JsonPart
        | TextPart
        | ToolCallPart
        | ToolResultPart
    ]
    session_id: None | str | Unset = UNSET
    task_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.artifact_ref_part import ArtifactRefPart
        from ..models.file_ref_part import FileRefPart
        from ..models.json_part import JsonPart
        from ..models.text_part import TextPart
        from ..models.tool_call_part import ToolCallPart
        from ..models.tool_result_part import ToolResultPart

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

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

        session_id: None | str | Unset
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        task_id: None | str | Unset
        if isinstance(self.task_id, Unset):
            task_id = UNSET
        else:
            task_id = self.task_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "role": role,
                "parts": parts,
            }
        )
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if task_id is not UNSET:
            field_dict["task_id"] = task_id

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
        id = d.pop("id")

        object_ = MessageObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        role = MessageRole(d.pop("role"))

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
                    componentsschemas_part_type_0 = TextPart.from_dict(data)

                    return componentsschemas_part_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_type_1 = JsonPart.from_dict(data)

                    return componentsschemas_part_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_type_2 = ToolCallPart.from_dict(data)

                    return componentsschemas_part_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_type_3 = ToolResultPart.from_dict(data)

                    return componentsschemas_part_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_type_4 = ArtifactRefPart.from_dict(data)

                    return componentsschemas_part_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_part_type_5 = FileRefPart.from_dict(data)

                    return componentsschemas_part_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_part_type_6 = ImageRefPart.from_dict(data)

                return componentsschemas_part_type_6

            parts_item = _parse_parts_item(parts_item_data)

            parts.append(parts_item)

        def _parse_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_task_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        task_id = _parse_task_id(d.pop("task_id", UNSET))

        message = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            role=role,
            parts=parts,
            session_id=session_id,
            task_id=task_id,
        )

        message.additional_properties = d
        return message

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
