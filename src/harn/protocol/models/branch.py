from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.branch_kind import BranchKind
from ..models.branch_object import BranchObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Branch")


@_attrs_define
class Branch:
    """
    Attributes:
        id (str):
        object_ (BranchObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        workspace_id (str):
        kind (BranchKind):
        base_ref (str):
        parent_branch_id (None | str | Unset):
        session_id (None | str | Unset):
        task_id (None | str | Unset):
        worktree_uri (None | str | Unset):
        created_by (None | str | Unset):
        merged_into (None | str | Unset):
    """

    id: str
    object_: BranchObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    workspace_id: str
    kind: BranchKind
    base_ref: str
    parent_branch_id: None | str | Unset = UNSET
    session_id: None | str | Unset = UNSET
    task_id: None | str | Unset = UNSET
    worktree_uri: None | str | Unset = UNSET
    created_by: None | str | Unset = UNSET
    merged_into: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        workspace_id = self.workspace_id

        kind = self.kind.value

        base_ref = self.base_ref

        parent_branch_id: None | str | Unset
        if isinstance(self.parent_branch_id, Unset):
            parent_branch_id = UNSET
        else:
            parent_branch_id = self.parent_branch_id

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

        worktree_uri: None | str | Unset
        if isinstance(self.worktree_uri, Unset):
            worktree_uri = UNSET
        else:
            worktree_uri = self.worktree_uri

        created_by: None | str | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        merged_into: None | str | Unset
        if isinstance(self.merged_into, Unset):
            merged_into = UNSET
        else:
            merged_into = self.merged_into

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "workspace_id": workspace_id,
                "kind": kind,
                "base_ref": base_ref,
            }
        )
        if parent_branch_id is not UNSET:
            field_dict["parent_branch_id"] = parent_branch_id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if worktree_uri is not UNSET:
            field_dict["worktree_uri"] = worktree_uri
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if merged_into is not UNSET:
            field_dict["merged_into"] = merged_into

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = BranchObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        workspace_id = d.pop("workspace_id")

        kind = BranchKind(d.pop("kind"))

        base_ref = d.pop("base_ref")

        def _parse_parent_branch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_branch_id = _parse_parent_branch_id(d.pop("parent_branch_id", UNSET))

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

        def _parse_worktree_uri(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        worktree_uri = _parse_worktree_uri(d.pop("worktree_uri", UNSET))

        def _parse_created_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_merged_into(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        merged_into = _parse_merged_into(d.pop("merged_into", UNSET))

        branch = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            workspace_id=workspace_id,
            kind=kind,
            base_ref=base_ref,
            parent_branch_id=parent_branch_id,
            session_id=session_id,
            task_id=task_id,
            worktree_uri=worktree_uri,
            created_by=created_by,
            merged_into=merged_into,
        )

        branch.additional_properties = d
        return branch

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
