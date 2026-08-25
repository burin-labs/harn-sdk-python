from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.harn_agent_card_object import HarnAgentCardObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.a2a_agent_card import A2AAgentCard
    from ..models.card_signature import CardSignature
    from ..models.harn_agent_interface import HarnAgentInterface
    from ..models.json_object import JsonObject
    from ..models.metadata import Metadata
    from ..models.quota import Quota
    from ..models.skill import Skill


T = TypeVar("T", bound="HarnAgentCard")


@_attrs_define
class HarnAgentCard:
    """
    Attributes:
        id (str):
        object_ (HarnAgentCardObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        name (str):
        description (str):
        protocol_version (str):
        a2a_card (A2AAgentCard):
        skills (list[Skill]):
        harn_interfaces (list[HarnAgentInterface] | Unset):
        persona_ids (list[str] | Unset):
        capabilities (list[str] | Unset):
        auth_schemes (list[str] | Unset):
        receipt_policy (None | str | Unset):
        quotas (list[Quota] | Unset):
        provider (JsonObject | Unset):
        public_url (None | str | Unset):
        signature (CardSignature | None | Unset):
    """

    id: str
    object_: HarnAgentCardObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    name: str
    description: str
    protocol_version: str
    a2a_card: A2AAgentCard
    skills: list[Skill]
    harn_interfaces: list[HarnAgentInterface] | Unset = UNSET
    persona_ids: list[str] | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    auth_schemes: list[str] | Unset = UNSET
    receipt_policy: None | str | Unset = UNSET
    quotas: list[Quota] | Unset = UNSET
    provider: JsonObject | Unset = UNSET
    public_url: None | str | Unset = UNSET
    signature: CardSignature | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.card_signature import CardSignature

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        name = self.name

        description = self.description

        protocol_version = self.protocol_version

        a2a_card = self.a2a_card.to_dict()

        skills = []
        for skills_item_data in self.skills:
            skills_item = skills_item_data.to_dict()
            skills.append(skills_item)

        harn_interfaces: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.harn_interfaces, Unset):
            harn_interfaces = []
            for harn_interfaces_item_data in self.harn_interfaces:
                harn_interfaces_item = harn_interfaces_item_data.to_dict()
                harn_interfaces.append(harn_interfaces_item)

        persona_ids: list[str] | Unset = UNSET
        if not isinstance(self.persona_ids, Unset):
            persona_ids = self.persona_ids

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        auth_schemes: list[str] | Unset = UNSET
        if not isinstance(self.auth_schemes, Unset):
            auth_schemes = self.auth_schemes

        receipt_policy: None | str | Unset
        if isinstance(self.receipt_policy, Unset):
            receipt_policy = UNSET
        else:
            receipt_policy = self.receipt_policy

        quotas: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.quotas, Unset):
            quotas = []
            for quotas_item_data in self.quotas:
                quotas_item = quotas_item_data.to_dict()
                quotas.append(quotas_item)

        provider: dict[str, Any] | Unset = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        public_url: None | str | Unset
        if isinstance(self.public_url, Unset):
            public_url = UNSET
        else:
            public_url = self.public_url

        signature: dict[str, Any] | None | Unset
        if isinstance(self.signature, Unset):
            signature = UNSET
        elif isinstance(self.signature, CardSignature):
            signature = self.signature.to_dict()
        else:
            signature = self.signature

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
                "protocol_version": protocol_version,
                "a2a_card": a2a_card,
                "skills": skills,
            }
        )
        if harn_interfaces is not UNSET:
            field_dict["harn_interfaces"] = harn_interfaces
        if persona_ids is not UNSET:
            field_dict["persona_ids"] = persona_ids
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if auth_schemes is not UNSET:
            field_dict["auth_schemes"] = auth_schemes
        if receipt_policy is not UNSET:
            field_dict["receipt_policy"] = receipt_policy
        if quotas is not UNSET:
            field_dict["quotas"] = quotas
        if provider is not UNSET:
            field_dict["provider"] = provider
        if public_url is not UNSET:
            field_dict["public_url"] = public_url
        if signature is not UNSET:
            field_dict["signature"] = signature

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.a2a_agent_card import A2AAgentCard
        from ..models.card_signature import CardSignature
        from ..models.harn_agent_interface import HarnAgentInterface
        from ..models.json_object import JsonObject
        from ..models.metadata import Metadata
        from ..models.quota import Quota
        from ..models.skill import Skill

        d = dict(src_dict)
        id = d.pop("id")

        object_ = HarnAgentCardObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        name = d.pop("name")

        description = d.pop("description")

        protocol_version = d.pop("protocol_version")

        a2a_card = A2AAgentCard.from_dict(d.pop("a2a_card"))

        skills = []
        _skills = d.pop("skills")
        for skills_item_data in _skills:
            skills_item = Skill.from_dict(skills_item_data)

            skills.append(skills_item)

        _harn_interfaces = d.pop("harn_interfaces", UNSET)
        harn_interfaces: list[HarnAgentInterface] | Unset = UNSET
        if _harn_interfaces is not UNSET:
            harn_interfaces = []
            for harn_interfaces_item_data in _harn_interfaces:
                harn_interfaces_item = HarnAgentInterface.from_dict(
                    harn_interfaces_item_data
                )

                harn_interfaces.append(harn_interfaces_item)

        persona_ids = cast(list[str], d.pop("persona_ids", UNSET))

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        auth_schemes = cast(list[str], d.pop("auth_schemes", UNSET))

        def _parse_receipt_policy(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        receipt_policy = _parse_receipt_policy(d.pop("receipt_policy", UNSET))

        _quotas = d.pop("quotas", UNSET)
        quotas: list[Quota] | Unset = UNSET
        if _quotas is not UNSET:
            quotas = []
            for quotas_item_data in _quotas:
                quotas_item = Quota.from_dict(quotas_item_data)

                quotas.append(quotas_item)

        _provider = d.pop("provider", UNSET)
        provider: JsonObject | Unset
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = JsonObject.from_dict(_provider)

        def _parse_public_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        public_url = _parse_public_url(d.pop("public_url", UNSET))

        def _parse_signature(data: object) -> CardSignature | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                signature_type_0 = CardSignature.from_dict(data)

                return signature_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CardSignature | None | Unset, data)

        signature = _parse_signature(d.pop("signature", UNSET))

        harn_agent_card = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            name=name,
            description=description,
            protocol_version=protocol_version,
            a2a_card=a2a_card,
            skills=skills,
            harn_interfaces=harn_interfaces,
            persona_ids=persona_ids,
            capabilities=capabilities,
            auth_schemes=auth_schemes,
            receipt_policy=receipt_policy,
            quotas=quotas,
            provider=provider,
            public_url=public_url,
            signature=signature,
        )

        harn_agent_card.additional_properties = d
        return harn_agent_card

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
