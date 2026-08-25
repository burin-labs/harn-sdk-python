from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.replay_mode import ReplayMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.replay_task_request_override import ReplayTaskRequestOverride


T = TypeVar("T", bound="ReplayTaskRequest")


@_attrs_define
class ReplayTaskRequest:
    """
    Attributes:
        mode (ReplayMode | Unset): `exact` reuses only recorded event-log material, `with_overrides`
            applies explicit substitutions, and `from_checkpoint` resumes from a
            recorded checkpoint before replaying later events.
        override (ReplayTaskRequestOverride | Unset): Map from stable override key to replacement replay material.
        checkpoint_id (None | str | Unset): Required when `mode` is `from_checkpoint` unless `checkpoint_event_id` is
            supplied.
        checkpoint_event_id (None | str | Unset): Event id of the checkpoint boundary for `from_checkpoint` replay.
        reason (None | str | Unset):
        metadata (Metadata | Unset):
    """

    mode: ReplayMode | Unset = UNSET
    override: ReplayTaskRequestOverride | Unset = UNSET
    checkpoint_id: None | str | Unset = UNSET
    checkpoint_event_id: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        override: dict[str, Any] | Unset = UNSET
        if not isinstance(self.override, Unset):
            override = self.override.to_dict()

        checkpoint_id: None | str | Unset
        if isinstance(self.checkpoint_id, Unset):
            checkpoint_id = UNSET
        else:
            checkpoint_id = self.checkpoint_id

        checkpoint_event_id: None | str | Unset
        if isinstance(self.checkpoint_event_id, Unset):
            checkpoint_event_id = UNSET
        else:
            checkpoint_event_id = self.checkpoint_event_id

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode
        if override is not UNSET:
            field_dict["override"] = override
        if checkpoint_id is not UNSET:
            field_dict["checkpoint_id"] = checkpoint_id
        if checkpoint_event_id is not UNSET:
            field_dict["checkpoint_event_id"] = checkpoint_event_id
        if reason is not UNSET:
            field_dict["reason"] = reason
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata
        from ..models.replay_task_request_override import ReplayTaskRequestOverride

        d = dict(src_dict)
        _mode = d.pop("mode", UNSET)
        mode: ReplayMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = ReplayMode(_mode)

        _override = d.pop("override", UNSET)
        override: ReplayTaskRequestOverride | Unset
        if isinstance(_override, Unset):
            override = UNSET
        else:
            override = ReplayTaskRequestOverride.from_dict(_override)

        def _parse_checkpoint_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        checkpoint_id = _parse_checkpoint_id(d.pop("checkpoint_id", UNSET))

        def _parse_checkpoint_event_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        checkpoint_event_id = _parse_checkpoint_event_id(
            d.pop("checkpoint_event_id", UNSET)
        )

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        replay_task_request = cls(
            mode=mode,
            override=override,
            checkpoint_id=checkpoint_id,
            checkpoint_event_id=checkpoint_event_id,
            reason=reason,
            metadata=metadata,
        )

        replay_task_request.additional_properties = d
        return replay_task_request

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
