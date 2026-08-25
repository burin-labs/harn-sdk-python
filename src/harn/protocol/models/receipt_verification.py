from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject


T = TypeVar("T", bound="ReceiptVerification")


@_attrs_define
class ReceiptVerification:
    """
    Attributes:
        valid (bool):
        checked_at (datetime.datetime):
        reason (None | str | Unset):
        details (JsonObject | Unset):
    """

    valid: bool
    checked_at: datetime.datetime
    reason: None | str | Unset = UNSET
    details: JsonObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        valid = self.valid

        checked_at = self.checked_at.isoformat()

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "valid": valid,
                "checked_at": checked_at,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject

        d = dict(src_dict)
        valid = d.pop("valid")

        checked_at = isoparse(d.pop("checked_at"))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        _details = d.pop("details", UNSET)
        details: JsonObject | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = JsonObject.from_dict(_details)

        receipt_verification = cls(
            valid=valid,
            checked_at=checked_at,
            reason=reason,
            details=details,
        )

        receipt_verification.additional_properties = d
        return receipt_verification

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
