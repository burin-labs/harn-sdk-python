from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.autonomy_tier import AutonomyTier
from ..models.persona_object import PersonaObject
from ..models.persona_receipt_policy import PersonaReceiptPolicy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Persona")


@_attrs_define
class Persona:
    """
    Attributes:
        id (str):
        object_ (PersonaObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        name (str):
        version (str):
        entry_workflow (str):
        description (str):
        autonomy_tier (AutonomyTier):
        receipt_policy (PersonaReceiptPolicy):
        tools (list[str] | Unset):
        capabilities (list[str] | Unset):
        triggers (list[JsonObject] | Unset):
        schedules (list[JsonObject] | Unset):
        handoffs (list[str] | Unset):
        context_packs (list[str] | Unset):
        evals (list[str] | Unset):
        owner (None | str | Unset):
        model_policy (JsonObject | Unset):
        rollout_policy (JsonObject | Unset):
        quota_id (None | str | Unset):
    """

    id: str
    object_: PersonaObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    name: str
    version: str
    entry_workflow: str
    description: str
    autonomy_tier: AutonomyTier
    receipt_policy: PersonaReceiptPolicy
    tools: list[str] | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    triggers: list[JsonObject] | Unset = UNSET
    schedules: list[JsonObject] | Unset = UNSET
    handoffs: list[str] | Unset = UNSET
    context_packs: list[str] | Unset = UNSET
    evals: list[str] | Unset = UNSET
    owner: None | str | Unset = UNSET
    model_policy: JsonObject | Unset = UNSET
    rollout_policy: JsonObject | Unset = UNSET
    quota_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        name = self.name

        version = self.version

        entry_workflow = self.entry_workflow

        description = self.description

        autonomy_tier = self.autonomy_tier.value

        receipt_policy = self.receipt_policy.value

        tools: list[str] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = self.tools

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        triggers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.triggers, Unset):
            triggers = []
            for triggers_item_data in self.triggers:
                triggers_item = triggers_item_data.to_dict()
                triggers.append(triggers_item)

        schedules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.schedules, Unset):
            schedules = []
            for schedules_item_data in self.schedules:
                schedules_item = schedules_item_data.to_dict()
                schedules.append(schedules_item)

        handoffs: list[str] | Unset = UNSET
        if not isinstance(self.handoffs, Unset):
            handoffs = self.handoffs

        context_packs: list[str] | Unset = UNSET
        if not isinstance(self.context_packs, Unset):
            context_packs = self.context_packs

        evals: list[str] | Unset = UNSET
        if not isinstance(self.evals, Unset):
            evals = self.evals

        owner: None | str | Unset
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        model_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.model_policy, Unset):
            model_policy = self.model_policy.to_dict()

        rollout_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rollout_policy, Unset):
            rollout_policy = self.rollout_policy.to_dict()

        quota_id: None | str | Unset
        if isinstance(self.quota_id, Unset):
            quota_id = UNSET
        else:
            quota_id = self.quota_id

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
                "version": version,
                "entry_workflow": entry_workflow,
                "description": description,
                "autonomy_tier": autonomy_tier,
                "receipt_policy": receipt_policy,
            }
        )
        if tools is not UNSET:
            field_dict["tools"] = tools
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if triggers is not UNSET:
            field_dict["triggers"] = triggers
        if schedules is not UNSET:
            field_dict["schedules"] = schedules
        if handoffs is not UNSET:
            field_dict["handoffs"] = handoffs
        if context_packs is not UNSET:
            field_dict["context_packs"] = context_packs
        if evals is not UNSET:
            field_dict["evals"] = evals
        if owner is not UNSET:
            field_dict["owner"] = owner
        if model_policy is not UNSET:
            field_dict["model_policy"] = model_policy
        if rollout_policy is not UNSET:
            field_dict["rollout_policy"] = rollout_policy
        if quota_id is not UNSET:
            field_dict["quota_id"] = quota_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = PersonaObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        name = d.pop("name")

        version = d.pop("version")

        entry_workflow = d.pop("entry_workflow")

        description = d.pop("description")

        autonomy_tier = AutonomyTier(d.pop("autonomy_tier"))

        receipt_policy = PersonaReceiptPolicy(d.pop("receipt_policy"))

        tools = cast(list[str], d.pop("tools", UNSET))

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        _triggers = d.pop("triggers", UNSET)
        triggers: list[JsonObject] | Unset = UNSET
        if _triggers is not UNSET:
            triggers = []
            for triggers_item_data in _triggers:
                triggers_item = JsonObject.from_dict(triggers_item_data)

                triggers.append(triggers_item)

        _schedules = d.pop("schedules", UNSET)
        schedules: list[JsonObject] | Unset = UNSET
        if _schedules is not UNSET:
            schedules = []
            for schedules_item_data in _schedules:
                schedules_item = JsonObject.from_dict(schedules_item_data)

                schedules.append(schedules_item)

        handoffs = cast(list[str], d.pop("handoffs", UNSET))

        context_packs = cast(list[str], d.pop("context_packs", UNSET))

        evals = cast(list[str], d.pop("evals", UNSET))

        def _parse_owner(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        owner = _parse_owner(d.pop("owner", UNSET))

        _model_policy = d.pop("model_policy", UNSET)
        model_policy: JsonObject | Unset
        if isinstance(_model_policy, Unset):
            model_policy = UNSET
        else:
            model_policy = JsonObject.from_dict(_model_policy)

        _rollout_policy = d.pop("rollout_policy", UNSET)
        rollout_policy: JsonObject | Unset
        if isinstance(_rollout_policy, Unset):
            rollout_policy = UNSET
        else:
            rollout_policy = JsonObject.from_dict(_rollout_policy)

        def _parse_quota_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        quota_id = _parse_quota_id(d.pop("quota_id", UNSET))

        persona = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            name=name,
            version=version,
            entry_workflow=entry_workflow,
            description=description,
            autonomy_tier=autonomy_tier,
            receipt_policy=receipt_policy,
            tools=tools,
            capabilities=capabilities,
            triggers=triggers,
            schedules=schedules,
            handoffs=handoffs,
            context_packs=context_packs,
            evals=evals,
            owner=owner,
            model_policy=model_policy,
            rollout_policy=rollout_policy,
            quota_id=quota_id,
        )

        persona.additional_properties = d
        return persona

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
