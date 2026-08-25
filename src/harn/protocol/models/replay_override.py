from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.replay_override_kind import ReplayOverrideKind
from ..models.replay_override_visibility import ReplayOverrideVisibility
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReplayOverride")


@_attrs_define
class ReplayOverride:
    """
    Attributes:
        kind (ReplayOverrideKind):
        event_id (None | str | Unset): Original EventLog event this override substitutes when known.
        target (None | str | Unset): Stable dependency key such as a model call id, tool call id, secret name, or clock
            label.
        value (Any | Unset): Any JSON value.
        artifact_id (None | str | Unset): Artifact containing replacement material when the value is large or receipt-
            only.
        sha256 (None | str | Unset):
        visibility (ReplayOverrideVisibility | Unset):  Default: ReplayOverrideVisibility.RECEIPT_ONLY.
        reason (None | str | Unset):
    """

    kind: ReplayOverrideKind
    event_id: None | str | Unset = UNSET
    target: None | str | Unset = UNSET
    value: Any | Unset = UNSET
    artifact_id: None | str | Unset = UNSET
    sha256: None | str | Unset = UNSET
    visibility: ReplayOverrideVisibility | Unset = ReplayOverrideVisibility.RECEIPT_ONLY
    reason: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        event_id: None | str | Unset
        if isinstance(self.event_id, Unset):
            event_id = UNSET
        else:
            event_id = self.event_id

        target: None | str | Unset
        if isinstance(self.target, Unset):
            target = UNSET
        else:
            target = self.target

        value = self.value

        artifact_id: None | str | Unset
        if isinstance(self.artifact_id, Unset):
            artifact_id = UNSET
        else:
            artifact_id = self.artifact_id

        sha256: None | str | Unset
        if isinstance(self.sha256, Unset):
            sha256 = UNSET
        else:
            sha256 = self.sha256

        visibility: str | Unset = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if target is not UNSET:
            field_dict["target"] = target
        if value is not UNSET:
            field_dict["value"] = value
        if artifact_id is not UNSET:
            field_dict["artifact_id"] = artifact_id
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = ReplayOverrideKind(d.pop("kind"))

        def _parse_event_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        event_id = _parse_event_id(d.pop("event_id", UNSET))

        def _parse_target(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target = _parse_target(d.pop("target", UNSET))

        value = d.pop("value", UNSET)

        def _parse_artifact_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        artifact_id = _parse_artifact_id(d.pop("artifact_id", UNSET))

        def _parse_sha256(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sha256 = _parse_sha256(d.pop("sha256", UNSET))

        _visibility = d.pop("visibility", UNSET)
        visibility: ReplayOverrideVisibility | Unset
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = ReplayOverrideVisibility(_visibility)

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        replay_override = cls(
            kind=kind,
            event_id=event_id,
            target=target,
            value=value,
            artifact_id=artifact_id,
            sha256=sha256,
            visibility=visibility,
            reason=reason,
        )

        replay_override.additional_properties = d
        return replay_override

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
