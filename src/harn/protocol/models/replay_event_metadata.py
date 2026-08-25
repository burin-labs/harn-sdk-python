from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.replay_mode import ReplayMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReplayEventMetadata")


@_attrs_define
class ReplayEventMetadata:
    """
    Attributes:
        source_task_id (str):
        replay_task_id (str):
        original_event_id (None | str | Unset):
        replay_cursor (None | str | Unset): Cursor clients can use when replay remaps event ids.
        mode (ReplayMode | Unset): `exact` reuses only recorded event-log material, `with_overrides`
            applies explicit substitutions, and `from_checkpoint` resumes from a
            recorded checkpoint before replaying later events.
        override_key (None | str | Unset): Override map key applied to produce this replayed event, when any.
        receipt_delta_id (None | str | Unset):
    """

    source_task_id: str
    replay_task_id: str
    original_event_id: None | str | Unset = UNSET
    replay_cursor: None | str | Unset = UNSET
    mode: ReplayMode | Unset = UNSET
    override_key: None | str | Unset = UNSET
    receipt_delta_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_task_id = self.source_task_id

        replay_task_id = self.replay_task_id

        original_event_id: None | str | Unset
        if isinstance(self.original_event_id, Unset):
            original_event_id = UNSET
        else:
            original_event_id = self.original_event_id

        replay_cursor: None | str | Unset
        if isinstance(self.replay_cursor, Unset):
            replay_cursor = UNSET
        else:
            replay_cursor = self.replay_cursor

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        override_key: None | str | Unset
        if isinstance(self.override_key, Unset):
            override_key = UNSET
        else:
            override_key = self.override_key

        receipt_delta_id: None | str | Unset
        if isinstance(self.receipt_delta_id, Unset):
            receipt_delta_id = UNSET
        else:
            receipt_delta_id = self.receipt_delta_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_task_id": source_task_id,
                "replay_task_id": replay_task_id,
            }
        )
        if original_event_id is not UNSET:
            field_dict["original_event_id"] = original_event_id
        if replay_cursor is not UNSET:
            field_dict["replay_cursor"] = replay_cursor
        if mode is not UNSET:
            field_dict["mode"] = mode
        if override_key is not UNSET:
            field_dict["override_key"] = override_key
        if receipt_delta_id is not UNSET:
            field_dict["receipt_delta_id"] = receipt_delta_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        source_task_id = d.pop("source_task_id")

        replay_task_id = d.pop("replay_task_id")

        def _parse_original_event_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        original_event_id = _parse_original_event_id(d.pop("original_event_id", UNSET))

        def _parse_replay_cursor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        replay_cursor = _parse_replay_cursor(d.pop("replay_cursor", UNSET))

        _mode = d.pop("mode", UNSET)
        mode: ReplayMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = ReplayMode(_mode)

        def _parse_override_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        override_key = _parse_override_key(d.pop("override_key", UNSET))

        def _parse_receipt_delta_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        receipt_delta_id = _parse_receipt_delta_id(d.pop("receipt_delta_id", UNSET))

        replay_event_metadata = cls(
            source_task_id=source_task_id,
            replay_task_id=replay_task_id,
            original_event_id=original_event_id,
            replay_cursor=replay_cursor,
            mode=mode,
            override_key=override_key,
            receipt_delta_id=receipt_delta_id,
        )

        replay_event_metadata.additional_properties = d
        return replay_event_metadata

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
