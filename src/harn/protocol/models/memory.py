from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.memory_object import MemoryObject
from ..models.memory_scope import MemoryScope
from ..models.part_visibility import PartVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_ref_part import ArtifactRefPart
    from ..models.json_object import JsonObject
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Memory")


@_attrs_define
class Memory:
    """
    Attributes:
        id (str):
        object_ (MemoryObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        scope (MemoryScope):
        owner_id (str):
        content (ArtifactRefPart | JsonObject | str):
        provenance (JsonObject):
        expires_at (datetime.datetime | None | Unset):
        embedding_ref (None | str | Unset):
        visibility (PartVisibility | Unset):
        redaction_policy (JsonObject | Unset):
        confidence (float | None | Unset):
    """

    id: str
    object_: MemoryObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    scope: MemoryScope
    owner_id: str
    content: ArtifactRefPart | JsonObject | str
    provenance: JsonObject
    expires_at: datetime.datetime | None | Unset = UNSET
    embedding_ref: None | str | Unset = UNSET
    visibility: PartVisibility | Unset = UNSET
    redaction_policy: JsonObject | Unset = UNSET
    confidence: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.artifact_ref_part import ArtifactRefPart
        from ..models.json_object import JsonObject

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        scope = self.scope.value

        owner_id = self.owner_id

        content: dict[str, Any] | str
        if isinstance(self.content, JsonObject) or isinstance(
            self.content, ArtifactRefPart
        ):
            content = self.content.to_dict()
        else:
            content = self.content

        provenance = self.provenance.to_dict()

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        embedding_ref: None | str | Unset
        if isinstance(self.embedding_ref, Unset):
            embedding_ref = UNSET
        else:
            embedding_ref = self.embedding_ref

        visibility: str | Unset = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        redaction_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.redaction_policy, Unset):
            redaction_policy = self.redaction_policy.to_dict()

        confidence: float | None | Unset
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "scope": scope,
                "owner_id": owner_id,
                "content": content,
                "provenance": provenance,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if embedding_ref is not UNSET:
            field_dict["embedding_ref"] = embedding_ref
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if redaction_policy is not UNSET:
            field_dict["redaction_policy"] = redaction_policy
        if confidence is not UNSET:
            field_dict["confidence"] = confidence

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.artifact_ref_part import ArtifactRefPart
        from ..models.json_object import JsonObject
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = MemoryObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        scope = MemoryScope(d.pop("scope"))

        owner_id = d.pop("owner_id")

        def _parse_content(data: object) -> ArtifactRefPart | JsonObject | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                content_type_1 = JsonObject.from_dict(data)

                return content_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                content_type_2 = ArtifactRefPart.from_dict(data)

                return content_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ArtifactRefPart | JsonObject | str, data)

        content = _parse_content(d.pop("content"))

        provenance = JsonObject.from_dict(d.pop("provenance"))

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_embedding_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        embedding_ref = _parse_embedding_ref(d.pop("embedding_ref", UNSET))

        _visibility = d.pop("visibility", UNSET)
        visibility: PartVisibility | Unset
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = PartVisibility(_visibility)

        _redaction_policy = d.pop("redaction_policy", UNSET)
        redaction_policy: JsonObject | Unset
        if isinstance(_redaction_policy, Unset):
            redaction_policy = UNSET
        else:
            redaction_policy = JsonObject.from_dict(_redaction_policy)

        def _parse_confidence(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        memory = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            scope=scope,
            owner_id=owner_id,
            content=content,
            provenance=provenance,
            expires_at=expires_at,
            embedding_ref=embedding_ref,
            visibility=visibility,
            redaction_policy=redaction_policy,
            confidence=confidence,
        )

        memory.additional_properties = d
        return memory

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
