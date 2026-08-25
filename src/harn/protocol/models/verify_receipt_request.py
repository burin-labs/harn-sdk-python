from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="VerifyReceiptRequest")


@_attrs_define
class VerifyReceiptRequest:
    """
    Attributes:
        trust_anchor (None | str | Unset):
        at_time (datetime.datetime | None | Unset):
    """

    trust_anchor: None | str | Unset = UNSET
    at_time: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trust_anchor: None | str | Unset
        if isinstance(self.trust_anchor, Unset):
            trust_anchor = UNSET
        else:
            trust_anchor = self.trust_anchor

        at_time: None | str | Unset
        if isinstance(self.at_time, Unset):
            at_time = UNSET
        elif isinstance(self.at_time, datetime.datetime):
            at_time = self.at_time.isoformat()
        else:
            at_time = self.at_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trust_anchor is not UNSET:
            field_dict["trust_anchor"] = trust_anchor
        if at_time is not UNSET:
            field_dict["at_time"] = at_time

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_trust_anchor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trust_anchor = _parse_trust_anchor(d.pop("trust_anchor", UNSET))

        def _parse_at_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                at_time_type_0 = isoparse(data)

                return at_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        at_time = _parse_at_time(d.pop("at_time", UNSET))

        verify_receipt_request = cls(
            trust_anchor=trust_anchor,
            at_time=at_time,
        )

        verify_receipt_request.additional_properties = d
        return verify_receipt_request

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
