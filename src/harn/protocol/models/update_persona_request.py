from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.update_persona_request_receipt_policy import (
    UpdatePersonaRequestReceiptPolicy,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="UpdatePersonaRequest")


@_attrs_define
class UpdatePersonaRequest:
    """
    Attributes:
        description (str | Unset):
        receipt_policy (UpdatePersonaRequestReceiptPolicy | Unset):
        quota_id (None | str | Unset):
        metadata (Metadata | Unset):
    """

    description: str | Unset = UNSET
    receipt_policy: UpdatePersonaRequestReceiptPolicy | Unset = UNSET
    quota_id: None | str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        receipt_policy: str | Unset = UNSET
        if not isinstance(self.receipt_policy, Unset):
            receipt_policy = self.receipt_policy.value

        quota_id: None | str | Unset
        if isinstance(self.quota_id, Unset):
            quota_id = UNSET
        else:
            quota_id = self.quota_id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if receipt_policy is not UNSET:
            field_dict["receipt_policy"] = receipt_policy
        if quota_id is not UNSET:
            field_dict["quota_id"] = quota_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        description = d.pop("description", UNSET)

        _receipt_policy = d.pop("receipt_policy", UNSET)
        receipt_policy: UpdatePersonaRequestReceiptPolicy | Unset
        if isinstance(_receipt_policy, Unset):
            receipt_policy = UNSET
        else:
            receipt_policy = UpdatePersonaRequestReceiptPolicy(_receipt_policy)

        def _parse_quota_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        quota_id = _parse_quota_id(d.pop("quota_id", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        update_persona_request = cls(
            description=description,
            receipt_policy=receipt_policy,
            quota_id=quota_id,
            metadata=metadata,
        )

        update_persona_request.additional_properties = d
        return update_persona_request

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
