from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject
    from ..models.message_input import MessageInput
    from ..models.metadata import Metadata


T = TypeVar("T", bound="SubmitTaskRequest")


@_attrs_define
class SubmitTaskRequest:
    """
    Attributes:
        input_ (JsonObject | MessageInput):
        session_id (str | Unset): Required on the top-level `/v1/tasks` submit path; inferred on nested Session paths.
        workspace_id (str | Unset):
        persona_id (None | str | Unset):
        branch_id (None | str | Unset):
        parent_task_id (None | str | Unset):
        metadata (Metadata | Unset):
    """

    input_: JsonObject | MessageInput
    session_id: str | Unset = UNSET
    workspace_id: str | Unset = UNSET
    persona_id: None | str | Unset = UNSET
    branch_id: None | str | Unset = UNSET
    parent_task_id: None | str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.message_input import MessageInput

        input_: dict[str, Any]
        if isinstance(self.input_, MessageInput):
            input_ = self.input_.to_dict()
        else:
            input_ = self.input_.to_dict()

        session_id = self.session_id

        workspace_id = self.workspace_id

        persona_id: None | str | Unset
        if isinstance(self.persona_id, Unset):
            persona_id = UNSET
        else:
            persona_id = self.persona_id

        branch_id: None | str | Unset
        if isinstance(self.branch_id, Unset):
            branch_id = UNSET
        else:
            branch_id = self.branch_id

        parent_task_id: None | str | Unset
        if isinstance(self.parent_task_id, Unset):
            parent_task_id = UNSET
        else:
            parent_task_id = self.parent_task_id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
            }
        )
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if persona_id is not UNSET:
            field_dict["persona_id"] = persona_id
        if branch_id is not UNSET:
            field_dict["branch_id"] = branch_id
        if parent_task_id is not UNSET:
            field_dict["parent_task_id"] = parent_task_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject
        from ..models.message_input import MessageInput
        from ..models.metadata import Metadata

        d = dict(src_dict)

        def _parse_input_(data: object) -> JsonObject | MessageInput:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_0 = MessageInput.from_dict(data)

                return input_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            input_type_1 = JsonObject.from_dict(data)

            return input_type_1

        input_ = _parse_input_(d.pop("input"))

        session_id = d.pop("session_id", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        def _parse_persona_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        persona_id = _parse_persona_id(d.pop("persona_id", UNSET))

        def _parse_branch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        branch_id = _parse_branch_id(d.pop("branch_id", UNSET))

        def _parse_parent_task_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_task_id = _parse_parent_task_id(d.pop("parent_task_id", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        submit_task_request = cls(
            input_=input_,
            session_id=session_id,
            workspace_id=workspace_id,
            persona_id=persona_id,
            branch_id=branch_id,
            parent_task_id=parent_task_id,
            metadata=metadata,
        )

        submit_task_request.additional_properties = d
        return submit_task_request

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
