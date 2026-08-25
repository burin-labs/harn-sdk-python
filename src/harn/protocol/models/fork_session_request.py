from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="ForkSessionRequest")


@_attrs_define
class ForkSessionRequest:
    """
    Attributes:
        at_event_id (None | str | Unset):
        branch_id (None | str | Unset):
        metadata (Metadata | Unset):
    """

    at_event_id: None | str | Unset = UNSET
    branch_id: None | str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at_event_id: None | str | Unset
        if isinstance(self.at_event_id, Unset):
            at_event_id = UNSET
        else:
            at_event_id = self.at_event_id

        branch_id: None | str | Unset
        if isinstance(self.branch_id, Unset):
            branch_id = UNSET
        else:
            branch_id = self.branch_id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if at_event_id is not UNSET:
            field_dict["at_event_id"] = at_event_id
        if branch_id is not UNSET:
            field_dict["branch_id"] = branch_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)

        def _parse_at_event_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        at_event_id = _parse_at_event_id(d.pop("at_event_id", UNSET))

        def _parse_branch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        branch_id = _parse_branch_id(d.pop("branch_id", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        fork_session_request = cls(
            at_event_id=at_event_id,
            branch_id=branch_id,
            metadata=metadata,
        )

        fork_session_request.additional_properties = d
        return fork_session_request

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
