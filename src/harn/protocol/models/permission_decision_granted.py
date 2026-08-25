from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.permission_decision_granted_outcome import (
    PermissionDecisionGrantedOutcome,
)
from ..models.permission_decision_granted_scope import PermissionDecisionGrantedScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionDecisionGranted")


@_attrs_define
class PermissionDecisionGranted:
    """
    Attributes:
        outcome (PermissionDecisionGrantedOutcome):
        scope (PermissionDecisionGrantedScope):
        policy_version (str):
        reason (None | str | Unset):
        expires_at (datetime.datetime | None | Unset):
        rule_id (None | str | Unset):
    """

    outcome: PermissionDecisionGrantedOutcome
    scope: PermissionDecisionGrantedScope
    policy_version: str
    reason: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    rule_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        outcome = self.outcome.value

        scope = self.scope.value

        policy_version = self.policy_version

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

        rule_id: None | str | Unset
        if isinstance(self.rule_id, Unset):
            rule_id = UNSET
        else:
            rule_id = self.rule_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "outcome": outcome,
                "scope": scope,
                "policy_version": policy_version,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if rule_id is not UNSET:
            field_dict["rule_id"] = rule_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        outcome = PermissionDecisionGrantedOutcome(d.pop("outcome"))

        scope = PermissionDecisionGrantedScope(d.pop("scope"))

        policy_version = d.pop("policy_version")

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

        def _parse_rule_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rule_id = _parse_rule_id(d.pop("rule_id", UNSET))

        permission_decision_granted = cls(
            outcome=outcome,
            scope=scope,
            policy_version=policy_version,
            reason=reason,
            expires_at=expires_at,
            rule_id=rule_id,
        )

        permission_decision_granted.additional_properties = d
        return permission_decision_granted

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
