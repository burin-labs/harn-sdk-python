from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.create_branch_request_kind import CreateBranchRequestKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="CreateBranchRequest")


@_attrs_define
class CreateBranchRequest:
    """
    Attributes:
        kind (CreateBranchRequestKind):
        base_ref (str):
        parent_branch_id (None | str | Unset):
        task_id (None | str | Unset):
        metadata (Metadata | Unset):
    """

    kind: CreateBranchRequestKind
    base_ref: str
    parent_branch_id: None | str | Unset = UNSET
    task_id: None | str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        base_ref = self.base_ref

        parent_branch_id: None | str | Unset
        if isinstance(self.parent_branch_id, Unset):
            parent_branch_id = UNSET
        else:
            parent_branch_id = self.parent_branch_id

        task_id: None | str | Unset
        if isinstance(self.task_id, Unset):
            task_id = UNSET
        else:
            task_id = self.task_id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "base_ref": base_ref,
            }
        )
        if parent_branch_id is not UNSET:
            field_dict["parent_branch_id"] = parent_branch_id
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        kind = CreateBranchRequestKind(d.pop("kind"))

        base_ref = d.pop("base_ref")

        def _parse_parent_branch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_branch_id = _parse_parent_branch_id(d.pop("parent_branch_id", UNSET))

        def _parse_task_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        task_id = _parse_task_id(d.pop("task_id", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        create_branch_request = cls(
            kind=kind,
            base_ref=base_ref,
            parent_branch_id=parent_branch_id,
            task_id=task_id,
            metadata=metadata,
        )

        create_branch_request.additional_properties = d
        return create_branch_request

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
