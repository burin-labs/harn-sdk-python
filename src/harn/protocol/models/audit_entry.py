from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.audit_entry_outcome import AuditEntryOutcome
from ..models.audit_entry_risk import AuditEntryRisk
from ..models.audit_entry_scope_type_1 import AuditEntryScopeType1
from ..models.audit_entry_scope_type_2_type_1 import AuditEntryScopeType2Type1
from ..models.audit_entry_scope_type_3_type_1 import AuditEntryScopeType3Type1
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission_check_request import PermissionCheckRequest


T = TypeVar("T", bound="AuditEntry")


@_attrs_define
class AuditEntry:
    """
    Attributes:
        request (PermissionCheckRequest):
        outcome (AuditEntryOutcome):
        policy_version (str):
        risk (AuditEntryRisk):
        decided_at (datetime.datetime):
        scope (AuditEntryScopeType1 | AuditEntryScopeType2Type1 | AuditEntryScopeType3Type1 | None | Unset):
        rule_id (None | str | Unset):
        reason (None | str | Unset):
        expires_at (datetime.datetime | None | Unset):
        decided_by (None | str | Unset):
    """

    request: PermissionCheckRequest
    outcome: AuditEntryOutcome
    policy_version: str
    risk: AuditEntryRisk
    decided_at: datetime.datetime
    scope: (
        AuditEntryScopeType1
        | AuditEntryScopeType2Type1
        | AuditEntryScopeType3Type1
        | None
        | Unset
    ) = UNSET
    rule_id: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    decided_by: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request = self.request.to_dict()

        outcome = self.outcome.value

        policy_version = self.policy_version

        risk = self.risk.value

        decided_at = self.decided_at.isoformat()

        scope: None | str | Unset
        if isinstance(self.scope, Unset):
            scope = UNSET
        elif (
            isinstance(self.scope, AuditEntryScopeType1)
            or isinstance(self.scope, AuditEntryScopeType2Type1)
            or isinstance(self.scope, AuditEntryScopeType3Type1)
        ):
            scope = self.scope.value
        else:
            scope = self.scope

        rule_id: None | str | Unset
        if isinstance(self.rule_id, Unset):
            rule_id = UNSET
        else:
            rule_id = self.rule_id

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        decided_by: None | str | Unset
        if isinstance(self.decided_by, Unset):
            decided_by = UNSET
        else:
            decided_by = self.decided_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request": request,
                "outcome": outcome,
                "policy_version": policy_version,
                "risk": risk,
                "decided_at": decided_at,
            }
        )
        if scope is not UNSET:
            field_dict["scope"] = scope
        if rule_id is not UNSET:
            field_dict["rule_id"] = rule_id
        if reason is not UNSET:
            field_dict["reason"] = reason
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if decided_by is not UNSET:
            field_dict["decided_by"] = decided_by

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.permission_check_request import PermissionCheckRequest

        d = dict(src_dict)
        request = PermissionCheckRequest.from_dict(d.pop("request"))

        outcome = AuditEntryOutcome(d.pop("outcome"))

        policy_version = d.pop("policy_version")

        risk = AuditEntryRisk(d.pop("risk"))

        decided_at = isoparse(d.pop("decided_at"))

        def _parse_scope(
            data: object,
        ) -> (
            AuditEntryScopeType1
            | AuditEntryScopeType2Type1
            | AuditEntryScopeType3Type1
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_1 = AuditEntryScopeType1(data)

                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_2_type_1 = AuditEntryScopeType2Type1(data)

                return scope_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_3_type_1 = AuditEntryScopeType3Type1(data)

                return scope_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                AuditEntryScopeType1
                | AuditEntryScopeType2Type1
                | AuditEntryScopeType3Type1
                | None
                | Unset,
                data,
            )

        scope = _parse_scope(d.pop("scope", UNSET))

        def _parse_rule_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rule_id = _parse_rule_id(d.pop("rule_id", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_decided_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        decided_by = _parse_decided_by(d.pop("decided_by", UNSET))

        audit_entry = cls(
            request=request,
            outcome=outcome,
            policy_version=policy_version,
            risk=risk,
            decided_at=decided_at,
            scope=scope,
            rule_id=rule_id,
            reason=reason,
            expires_at=expires_at,
            decided_by=decided_by,
        )

        audit_entry.additional_properties = d
        return audit_entry

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
