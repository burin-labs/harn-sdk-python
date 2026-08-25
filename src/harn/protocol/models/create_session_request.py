from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message_input import MessageInput
    from ..models.metadata import Metadata
    from ..models.session_model_policy import SessionModelPolicy


T = TypeVar("T", bound="CreateSessionRequest")


@_attrs_define
class CreateSessionRequest:
    """
    Attributes:
        workspace_id (str):
        persona_id (None | str | Unset):
        model_policy (None | SessionModelPolicy | Unset): Optional session model default. Null is equivalent to
            omission.
        vault_ids (list[str] | Unset):
        memory_ids (list[str] | Unset):
        skill_ids (list[str] | Unset):
        initial_messages (list[MessageInput] | Unset):
        metadata (Metadata | Unset):
    """

    workspace_id: str
    persona_id: None | str | Unset = UNSET
    model_policy: None | SessionModelPolicy | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET
    memory_ids: list[str] | Unset = UNSET
    skill_ids: list[str] | Unset = UNSET
    initial_messages: list[MessageInput] | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.session_model_policy import SessionModelPolicy

        workspace_id = self.workspace_id

        persona_id: None | str | Unset
        if isinstance(self.persona_id, Unset):
            persona_id = UNSET
        else:
            persona_id = self.persona_id

        model_policy: dict[str, Any] | None | Unset
        if isinstance(self.model_policy, Unset):
            model_policy = UNSET
        elif isinstance(self.model_policy, SessionModelPolicy):
            model_policy = self.model_policy.to_dict()
        else:
            model_policy = self.model_policy

        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids

        memory_ids: list[str] | Unset = UNSET
        if not isinstance(self.memory_ids, Unset):
            memory_ids = self.memory_ids

        skill_ids: list[str] | Unset = UNSET
        if not isinstance(self.skill_ids, Unset):
            skill_ids = self.skill_ids

        initial_messages: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.initial_messages, Unset):
            initial_messages = []
            for initial_messages_item_data in self.initial_messages:
                initial_messages_item = initial_messages_item_data.to_dict()
                initial_messages.append(initial_messages_item)

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
            }
        )
        if persona_id is not UNSET:
            field_dict["persona_id"] = persona_id
        if model_policy is not UNSET:
            field_dict["model_policy"] = model_policy
        if vault_ids is not UNSET:
            field_dict["vault_ids"] = vault_ids
        if memory_ids is not UNSET:
            field_dict["memory_ids"] = memory_ids
        if skill_ids is not UNSET:
            field_dict["skill_ids"] = skill_ids
        if initial_messages is not UNSET:
            field_dict["initial_messages"] = initial_messages
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.message_input import MessageInput
        from ..models.metadata import Metadata
        from ..models.session_model_policy import SessionModelPolicy

        d = dict(src_dict)
        workspace_id = d.pop("workspace_id")

        def _parse_persona_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        persona_id = _parse_persona_id(d.pop("persona_id", UNSET))

        def _parse_model_policy(data: object) -> None | SessionModelPolicy | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_policy_type_0 = SessionModelPolicy.from_dict(data)

                return model_policy_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SessionModelPolicy | Unset, data)

        model_policy = _parse_model_policy(d.pop("model_policy", UNSET))

        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))

        memory_ids = cast(list[str], d.pop("memory_ids", UNSET))

        skill_ids = cast(list[str], d.pop("skill_ids", UNSET))

        _initial_messages = d.pop("initial_messages", UNSET)
        initial_messages: list[MessageInput] | Unset = UNSET
        if _initial_messages is not UNSET:
            initial_messages = []
            for initial_messages_item_data in _initial_messages:
                initial_messages_item = MessageInput.from_dict(
                    initial_messages_item_data
                )

                initial_messages.append(initial_messages_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        create_session_request = cls(
            workspace_id=workspace_id,
            persona_id=persona_id,
            model_policy=model_policy,
            vault_ids=vault_ids,
            memory_ids=memory_ids,
            skill_ids=skill_ids,
            initial_messages=initial_messages,
            metadata=metadata,
        )

        create_session_request.additional_properties = d
        return create_session_request

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
