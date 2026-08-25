from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.workspace_file_entry_kind import WorkspaceFileEntryKind

T = TypeVar("T", bound="WorkspaceFileEntry")


@_attrs_define
class WorkspaceFileEntry:
    """
    Attributes:
        name (str):
        path (str):
        kind (WorkspaceFileEntryKind):
        size (int):
    """

    name: str
    path: str
    kind: WorkspaceFileEntryKind
    size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        path = self.path

        kind = self.kind.value

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "path": path,
                "kind": kind,
                "size": size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        path = d.pop("path")

        kind = WorkspaceFileEntryKind(d.pop("kind"))

        size = d.pop("size")

        workspace_file_entry = cls(
            name=name,
            path=path,
            kind=kind,
            size=size,
        )

        workspace_file_entry.additional_properties = d
        return workspace_file_entry

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
