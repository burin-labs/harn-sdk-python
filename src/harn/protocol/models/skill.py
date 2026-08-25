from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.skill_object import SkillObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Skill")


@_attrs_define
class Skill:
    """
    Attributes:
        id (str):
        object_ (SkillObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        name (str):
        description (str):
        input_schema (JsonObject | None):
        output_schema (JsonObject | None):
        source (None | str | Unset):
        version (None | str | Unset):
        capabilities (list[str] | Unset):
        requires_approval (bool | Unset):  Default: False.
        deprecated (bool | Unset):  Default: False.
    """

    id: str
    object_: SkillObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    name: str
    description: str
    input_schema: JsonObject | None
    output_schema: JsonObject | None
    source: None | str | Unset = UNSET
    version: None | str | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    requires_approval: bool | Unset = False
    deprecated: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.json_object import JsonObject

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        name = self.name

        description = self.description

        input_schema: dict[str, Any] | None
        if isinstance(self.input_schema, JsonObject):
            input_schema = self.input_schema.to_dict()
        else:
            input_schema = self.input_schema

        output_schema: dict[str, Any] | None
        if isinstance(self.output_schema, JsonObject):
            output_schema = self.output_schema.to_dict()
        else:
            output_schema = self.output_schema

        source: None | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        version: None | str | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        requires_approval = self.requires_approval

        deprecated = self.deprecated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "name": name,
                "description": description,
                "input_schema": input_schema,
                "output_schema": output_schema,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if version is not UNSET:
            field_dict["version"] = version
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if requires_approval is not UNSET:
            field_dict["requires_approval"] = requires_approval
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = SkillObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        name = d.pop("name")

        description = d.pop("description")

        def _parse_input_schema(data: object) -> JsonObject | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_schema_type_0 = JsonObject.from_dict(data)

                return input_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JsonObject | None, data)

        input_schema = _parse_input_schema(d.pop("input_schema"))

        def _parse_output_schema(data: object) -> JsonObject | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_schema_type_0 = JsonObject.from_dict(data)

                return output_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JsonObject | None, data)

        output_schema = _parse_output_schema(d.pop("output_schema"))

        def _parse_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        def _parse_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        requires_approval = d.pop("requires_approval", UNSET)

        deprecated = d.pop("deprecated", UNSET)

        skill = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            source=source,
            version=version,
            capabilities=capabilities,
            requires_approval=requires_approval,
            deprecated=deprecated,
        )

        skill.additional_properties = d
        return skill

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
