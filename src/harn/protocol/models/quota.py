from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.quota_object import QuotaObject
from ..models.quota_scope import QuotaScope
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.quota_limits import QuotaLimits
    from ..models.quota_usage import QuotaUsage


T = TypeVar("T", bound="Quota")


@_attrs_define
class Quota:
    """
    Attributes:
        id (str):
        object_ (QuotaObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        scope (QuotaScope):
        limits (QuotaLimits):
        usage (QuotaUsage):
        reset_at (datetime.datetime | None | Unset):
        hard_limit (bool | Unset):  Default: True.
        soft_limit (bool | Unset):  Default: False.
        exhaustion_reason (None | str | Unset):
        last_receipt_id (None | str | Unset):
    """

    id: str
    object_: QuotaObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    scope: QuotaScope
    limits: QuotaLimits
    usage: QuotaUsage
    reset_at: datetime.datetime | None | Unset = UNSET
    hard_limit: bool | Unset = True
    soft_limit: bool | Unset = False
    exhaustion_reason: None | str | Unset = UNSET
    last_receipt_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        scope = self.scope.value

        limits = self.limits.to_dict()

        usage = self.usage.to_dict()

        reset_at: None | str | Unset
        if isinstance(self.reset_at, Unset):
            reset_at = UNSET
        elif isinstance(self.reset_at, datetime.datetime):
            reset_at = self.reset_at.isoformat()
        else:
            reset_at = self.reset_at

        hard_limit = self.hard_limit

        soft_limit = self.soft_limit

        exhaustion_reason: None | str | Unset
        if isinstance(self.exhaustion_reason, Unset):
            exhaustion_reason = UNSET
        else:
            exhaustion_reason = self.exhaustion_reason

        last_receipt_id: None | str | Unset
        if isinstance(self.last_receipt_id, Unset):
            last_receipt_id = UNSET
        else:
            last_receipt_id = self.last_receipt_id

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
                "limits": limits,
                "usage": usage,
            }
        )
        if reset_at is not UNSET:
            field_dict["reset_at"] = reset_at
        if hard_limit is not UNSET:
            field_dict["hard_limit"] = hard_limit
        if soft_limit is not UNSET:
            field_dict["soft_limit"] = soft_limit
        if exhaustion_reason is not UNSET:
            field_dict["exhaustion_reason"] = exhaustion_reason
        if last_receipt_id is not UNSET:
            field_dict["last_receipt_id"] = last_receipt_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata
        from ..models.quota_limits import QuotaLimits
        from ..models.quota_usage import QuotaUsage

        d = dict(src_dict)
        id = d.pop("id")

        object_ = QuotaObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        scope = QuotaScope(d.pop("scope"))

        limits = QuotaLimits.from_dict(d.pop("limits"))

        usage = QuotaUsage.from_dict(d.pop("usage"))

        def _parse_reset_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reset_at_type_0 = isoparse(data)

                return reset_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        reset_at = _parse_reset_at(d.pop("reset_at", UNSET))

        hard_limit = d.pop("hard_limit", UNSET)

        soft_limit = d.pop("soft_limit", UNSET)

        def _parse_exhaustion_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        exhaustion_reason = _parse_exhaustion_reason(d.pop("exhaustion_reason", UNSET))

        def _parse_last_receipt_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_receipt_id = _parse_last_receipt_id(d.pop("last_receipt_id", UNSET))

        quota = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            scope=scope,
            limits=limits,
            usage=usage,
            reset_at=reset_at,
            hard_limit=hard_limit,
            soft_limit=soft_limit,
            exhaustion_reason=exhaustion_reason,
            last_receipt_id=last_receipt_id,
        )

        quota.additional_properties = d
        return quota

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
