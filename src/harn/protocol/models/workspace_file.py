from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.workspace_file_encoding import WorkspaceFileEncoding
from ..models.workspace_file_object import WorkspaceFileObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceFile")


@_attrs_define
class WorkspaceFile:
    """
    Attributes:
        object_ (WorkspaceFileObject):
        workspace_id (str):
        path (str):
        encoding (WorkspaceFileEncoding):
        content (str | Unset):
        bytes_ (int | Unset):
    """

    object_: WorkspaceFileObject
    workspace_id: str
    path: str
    encoding: WorkspaceFileEncoding
    content: str | Unset = UNSET
    bytes_: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        workspace_id = self.workspace_id

        path = self.path

        encoding = self.encoding.value

        content = self.content

        bytes_ = self.bytes_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "workspace_id": workspace_id,
                "path": path,
                "encoding": encoding,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content
        if bytes_ is not UNSET:
            field_dict["bytes"] = bytes_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        object_ = WorkspaceFileObject(d.pop("object"))

        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        encoding = WorkspaceFileEncoding(d.pop("encoding"))

        content = d.pop("content", UNSET)

        bytes_ = d.pop("bytes", UNSET)

        workspace_file = cls(
            object_=object_,
            workspace_id=workspace_id,
            path=path,
            encoding=encoding,
            content=content,
            bytes_=bytes_,
        )

        workspace_file.additional_properties = d
        return workspace_file

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
