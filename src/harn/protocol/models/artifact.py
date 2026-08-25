from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.artifact_kind import ArtifactKind
from ..models.artifact_object import ArtifactObject
from ..models.part_visibility import PartVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Artifact")


@_attrs_define
class Artifact:
    """
    Attributes:
        id (str):
        object_ (ArtifactObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        kind (ArtifactKind):
        mime_type (str):
        uri (None | str):
        visibility (PartVisibility):
        sha256 (None | str):
        workspace_id (None | str | Unset):
        session_id (None | str | Unset):
        task_id (None | str | Unset):
        receipt_id (None | str | Unset):
    """

    id: str
    object_: ArtifactObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    kind: ArtifactKind
    mime_type: str
    uri: None | str
    visibility: PartVisibility
    sha256: None | str
    workspace_id: None | str | Unset = UNSET
    session_id: None | str | Unset = UNSET
    task_id: None | str | Unset = UNSET
    receipt_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        kind = self.kind.value

        mime_type = self.mime_type

        uri: None | str
        uri = self.uri

        visibility = self.visibility.value

        sha256: None | str
        sha256 = self.sha256

        workspace_id: None | str | Unset
        if isinstance(self.workspace_id, Unset):
            workspace_id = UNSET
        else:
            workspace_id = self.workspace_id

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

        receipt_id: None | str | Unset
        if isinstance(self.receipt_id, Unset):
            receipt_id = UNSET
        else:
            receipt_id = self.receipt_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "kind": kind,
                "mime_type": mime_type,
                "uri": uri,
                "visibility": visibility,
                "sha256": sha256,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if receipt_id is not UNSET:
            field_dict["receipt_id"] = receipt_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = ArtifactObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        kind = ArtifactKind(d.pop("kind"))

        mime_type = d.pop("mime_type")

        def _parse_uri(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        uri = _parse_uri(d.pop("uri"))

        visibility = PartVisibility(d.pop("visibility"))

        def _parse_sha256(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        sha256 = _parse_sha256(d.pop("sha256"))

        def _parse_workspace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        workspace_id = _parse_workspace_id(d.pop("workspace_id", UNSET))

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

        def _parse_receipt_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        receipt_id = _parse_receipt_id(d.pop("receipt_id", UNSET))

        artifact = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            kind=kind,
            mime_type=mime_type,
            uri=uri,
            visibility=visibility,
            sha256=sha256,
            workspace_id=workspace_id,
            session_id=session_id,
            task_id=task_id,
            receipt_id=receipt_id,
        )

        artifact.additional_properties = d
        return artifact

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
