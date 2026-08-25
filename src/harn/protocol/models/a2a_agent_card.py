from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.a2a_agent_capabilities import A2AAgentCapabilities
    from ..models.a2a_agent_card_security_item import A2AAgentCardSecurityItem
    from ..models.a2a_agent_card_security_schemes import A2AAgentCardSecuritySchemes
    from ..models.a2a_agent_card_signature import A2AAgentCardSignature
    from ..models.a2a_agent_interface import A2AAgentInterface
    from ..models.a2a_agent_provider import A2AAgentProvider
    from ..models.a2a_agent_skill import A2AAgentSkill


T = TypeVar("T", bound="A2AAgentCard")


@_attrs_define
class A2AAgentCard:
    """
    Attributes:
        name (str):
        description (str):
        supported_interfaces (list[A2AAgentInterface]):
        version (str):
        capabilities (A2AAgentCapabilities):
        default_input_modes (list[str]):
        default_output_modes (list[str]):
        skills (list[A2AAgentSkill]):
        provider (A2AAgentProvider | Unset):
        documentation_url (None | str | Unset):
        security_schemes (A2AAgentCardSecuritySchemes | Unset):
        security (list[A2AAgentCardSecurityItem] | Unset):
        signatures (list[A2AAgentCardSignature] | Unset):
        icon_url (None | str | Unset):
    """

    name: str
    description: str
    supported_interfaces: list[A2AAgentInterface]
    version: str
    capabilities: A2AAgentCapabilities
    default_input_modes: list[str]
    default_output_modes: list[str]
    skills: list[A2AAgentSkill]
    provider: A2AAgentProvider | Unset = UNSET
    documentation_url: None | str | Unset = UNSET
    security_schemes: A2AAgentCardSecuritySchemes | Unset = UNSET
    security: list[A2AAgentCardSecurityItem] | Unset = UNSET
    signatures: list[A2AAgentCardSignature] | Unset = UNSET
    icon_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        supported_interfaces = []
        for supported_interfaces_item_data in self.supported_interfaces:
            supported_interfaces_item = supported_interfaces_item_data.to_dict()
            supported_interfaces.append(supported_interfaces_item)

        version = self.version

        capabilities = self.capabilities.to_dict()

        default_input_modes = self.default_input_modes

        default_output_modes = self.default_output_modes

        skills = []
        for skills_item_data in self.skills:
            skills_item = skills_item_data.to_dict()
            skills.append(skills_item)

        provider: dict[str, Any] | Unset = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        documentation_url: None | str | Unset
        if isinstance(self.documentation_url, Unset):
            documentation_url = UNSET
        else:
            documentation_url = self.documentation_url

        security_schemes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.security_schemes, Unset):
            security_schemes = self.security_schemes.to_dict()

        security: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.security, Unset):
            security = []
            for security_item_data in self.security:
                security_item = security_item_data.to_dict()
                security.append(security_item)

        signatures: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.signatures, Unset):
            signatures = []
            for signatures_item_data in self.signatures:
                signatures_item = signatures_item_data.to_dict()
                signatures.append(signatures_item)

        icon_url: None | str | Unset
        if isinstance(self.icon_url, Unset):
            icon_url = UNSET
        else:
            icon_url = self.icon_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "supportedInterfaces": supported_interfaces,
                "version": version,
                "capabilities": capabilities,
                "defaultInputModes": default_input_modes,
                "defaultOutputModes": default_output_modes,
                "skills": skills,
            }
        )
        if provider is not UNSET:
            field_dict["provider"] = provider
        if documentation_url is not UNSET:
            field_dict["documentationUrl"] = documentation_url
        if security_schemes is not UNSET:
            field_dict["securitySchemes"] = security_schemes
        if security is not UNSET:
            field_dict["security"] = security
        if signatures is not UNSET:
            field_dict["signatures"] = signatures
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.a2a_agent_capabilities import A2AAgentCapabilities
        from ..models.a2a_agent_card_security_item import A2AAgentCardSecurityItem
        from ..models.a2a_agent_card_security_schemes import A2AAgentCardSecuritySchemes
        from ..models.a2a_agent_card_signature import A2AAgentCardSignature
        from ..models.a2a_agent_interface import A2AAgentInterface
        from ..models.a2a_agent_provider import A2AAgentProvider
        from ..models.a2a_agent_skill import A2AAgentSkill

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        supported_interfaces = []
        _supported_interfaces = d.pop("supportedInterfaces")
        for supported_interfaces_item_data in _supported_interfaces:
            supported_interfaces_item = A2AAgentInterface.from_dict(
                supported_interfaces_item_data
            )

            supported_interfaces.append(supported_interfaces_item)

        version = d.pop("version")

        capabilities = A2AAgentCapabilities.from_dict(d.pop("capabilities"))

        default_input_modes = cast(list[str], d.pop("defaultInputModes"))

        default_output_modes = cast(list[str], d.pop("defaultOutputModes"))

        skills = []
        _skills = d.pop("skills")
        for skills_item_data in _skills:
            skills_item = A2AAgentSkill.from_dict(skills_item_data)

            skills.append(skills_item)

        _provider = d.pop("provider", UNSET)
        provider: A2AAgentProvider | Unset
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = A2AAgentProvider.from_dict(_provider)

        def _parse_documentation_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        documentation_url = _parse_documentation_url(d.pop("documentationUrl", UNSET))

        _security_schemes = d.pop("securitySchemes", UNSET)
        security_schemes: A2AAgentCardSecuritySchemes | Unset
        if isinstance(_security_schemes, Unset):
            security_schemes = UNSET
        else:
            security_schemes = A2AAgentCardSecuritySchemes.from_dict(_security_schemes)

        _security = d.pop("security", UNSET)
        security: list[A2AAgentCardSecurityItem] | Unset = UNSET
        if _security is not UNSET:
            security = []
            for security_item_data in _security:
                security_item = A2AAgentCardSecurityItem.from_dict(security_item_data)

                security.append(security_item)

        _signatures = d.pop("signatures", UNSET)
        signatures: list[A2AAgentCardSignature] | Unset = UNSET
        if _signatures is not UNSET:
            signatures = []
            for signatures_item_data in _signatures:
                signatures_item = A2AAgentCardSignature.from_dict(signatures_item_data)

                signatures.append(signatures_item)

        def _parse_icon_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icon_url = _parse_icon_url(d.pop("iconUrl", UNSET))

        a2a_agent_card = cls(
            name=name,
            description=description,
            supported_interfaces=supported_interfaces,
            version=version,
            capabilities=capabilities,
            default_input_modes=default_input_modes,
            default_output_modes=default_output_modes,
            skills=skills,
            provider=provider,
            documentation_url=documentation_url,
            security_schemes=security_schemes,
            security=security,
            signatures=signatures,
            icon_url=icon_url,
        )

        a2a_agent_card.additional_properties = d
        return a2a_agent_card

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
