from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.workspace_file_listing_object import WorkspaceFileListingObject

if TYPE_CHECKING:
    from ..models.workspace_file_entry import WorkspaceFileEntry


T = TypeVar("T", bound="WorkspaceFileListing")


@_attrs_define
class WorkspaceFileListing:
    """
    Attributes:
        object_ (WorkspaceFileListingObject):
        workspace_id (str):
        path (str):
        entries (list[WorkspaceFileEntry]):
    """

    object_: WorkspaceFileListingObject
    workspace_id: str
    path: str
    entries: list[WorkspaceFileEntry]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        workspace_id = self.workspace_id

        path = self.path

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "workspace_id": workspace_id,
                "path": path,
                "entries": entries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_file_entry import WorkspaceFileEntry

        d = dict(src_dict)
        object_ = WorkspaceFileListingObject(d.pop("object"))

        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = WorkspaceFileEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        workspace_file_listing = cls(
            object_=object_,
            workspace_id=workspace_id,
            path=path,
            entries=entries,
        )

        workspace_file_listing.additional_properties = d
        return workspace_file_listing

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
