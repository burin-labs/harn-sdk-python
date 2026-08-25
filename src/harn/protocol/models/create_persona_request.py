from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.autonomy_tier import AutonomyTier
from ..models.create_persona_request_receipt_policy import (
    CreatePersonaRequestReceiptPolicy,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="CreatePersonaRequest")


@_attrs_define
class CreatePersonaRequest:
    """
    Attributes:
        name (str):
        version (str):
        entry_workflow (str):
        description (str):
        autonomy_tier (AutonomyTier):
        receipt_policy (CreatePersonaRequestReceiptPolicy):
        module_ref (str | Unset): Optional harn://owner/name@version module reference.
        metadata (Metadata | Unset):
    """

    name: str
    version: str
    entry_workflow: str
    description: str
    autonomy_tier: AutonomyTier
    receipt_policy: CreatePersonaRequestReceiptPolicy
    module_ref: str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        entry_workflow = self.entry_workflow

        description = self.description

        autonomy_tier = self.autonomy_tier.value

        receipt_policy = self.receipt_policy.value

        module_ref = self.module_ref

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "entry_workflow": entry_workflow,
                "description": description,
                "autonomy_tier": autonomy_tier,
                "receipt_policy": receipt_policy,
            }
        )
        if module_ref is not UNSET:
            field_dict["module_ref"] = module_ref
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        entry_workflow = d.pop("entry_workflow")

        description = d.pop("description")

        autonomy_tier = AutonomyTier(d.pop("autonomy_tier"))

        receipt_policy = CreatePersonaRequestReceiptPolicy(d.pop("receipt_policy"))

        module_ref = d.pop("module_ref", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        create_persona_request = cls(
            name=name,
            version=version,
            entry_workflow=entry_workflow,
            description=description,
            autonomy_tier=autonomy_tier,
            receipt_policy=receipt_policy,
            module_ref=module_ref,
            metadata=metadata,
        )

        create_persona_request.additional_properties = d
        return create_persona_request

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
