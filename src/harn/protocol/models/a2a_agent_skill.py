from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.a2a_agent_skill_security_item import A2AAgentSkillSecurityItem
    from ..models.json_object import JsonObject


T = TypeVar("T", bound="A2AAgentSkill")


@_attrs_define
class A2AAgentSkill:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        tags (list[str]):
        examples (list[str] | Unset):
        input_modes (list[str] | Unset):
        output_modes (list[str] | Unset):
        security (list[A2AAgentSkillSecurityItem] | Unset):
        input_schema (JsonObject | None | Unset):
    """

    id: str
    name: str
    description: str
    tags: list[str]
    examples: list[str] | Unset = UNSET
    input_modes: list[str] | Unset = UNSET
    output_modes: list[str] | Unset = UNSET
    security: list[A2AAgentSkillSecurityItem] | Unset = UNSET
    input_schema: JsonObject | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.json_object import JsonObject

        id = self.id

        name = self.name

        description = self.description

        tags = self.tags

        examples: list[str] | Unset = UNSET
        if not isinstance(self.examples, Unset):
            examples = self.examples

        input_modes: list[str] | Unset = UNSET
        if not isinstance(self.input_modes, Unset):
            input_modes = self.input_modes

        output_modes: list[str] | Unset = UNSET
        if not isinstance(self.output_modes, Unset):
            output_modes = self.output_modes

        security: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.security, Unset):
            security = []
            for security_item_data in self.security:
                security_item = security_item_data.to_dict()
                security.append(security_item)

        input_schema: dict[str, Any] | None | Unset
        if isinstance(self.input_schema, Unset):
            input_schema = UNSET
        elif isinstance(self.input_schema, JsonObject):
            input_schema = self.input_schema.to_dict()
        else:
            input_schema = self.input_schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "tags": tags,
            }
        )
        if examples is not UNSET:
            field_dict["examples"] = examples
        if input_modes is not UNSET:
            field_dict["inputModes"] = input_modes
        if output_modes is not UNSET:
            field_dict["outputModes"] = output_modes
        if security is not UNSET:
            field_dict["security"] = security
        if input_schema is not UNSET:
            field_dict["inputSchema"] = input_schema

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.a2a_agent_skill_security_item import A2AAgentSkillSecurityItem
        from ..models.json_object import JsonObject

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        tags = cast(list[str], d.pop("tags"))

        examples = cast(list[str], d.pop("examples", UNSET))

        input_modes = cast(list[str], d.pop("inputModes", UNSET))

        output_modes = cast(list[str], d.pop("outputModes", UNSET))

        _security = d.pop("security", UNSET)
        security: list[A2AAgentSkillSecurityItem] | Unset = UNSET
        if _security is not UNSET:
            security = []
            for security_item_data in _security:
                security_item = A2AAgentSkillSecurityItem.from_dict(security_item_data)

                security.append(security_item)

        def _parse_input_schema(data: object) -> JsonObject | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_schema_type_0 = JsonObject.from_dict(data)

                return input_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JsonObject | None | Unset, data)

        input_schema = _parse_input_schema(d.pop("inputSchema", UNSET))

        a2a_agent_skill = cls(
            id=id,
            name=name,
            description=description,
            tags=tags,
            examples=examples,
            input_modes=input_modes,
            output_modes=output_modes,
            security=security,
            input_schema=input_schema,
        )

        a2a_agent_skill.additional_properties = d
        return a2a_agent_skill

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
