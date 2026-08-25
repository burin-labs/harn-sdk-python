from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.permission_decision_denied_outcome import PermissionDecisionDeniedOutcome
from ..models.permission_decision_denied_scope import PermissionDecisionDeniedScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionDecisionDenied")


@_attrs_define
class PermissionDecisionDenied:
    """
    Attributes:
        outcome (PermissionDecisionDeniedOutcome):
        scope (PermissionDecisionDeniedScope):
        policy_version (str):
        reason (None | str | Unset):
        rule_id (None | str | Unset):
    """

    outcome: PermissionDecisionDeniedOutcome
    scope: PermissionDecisionDeniedScope
    policy_version: str
    reason: None | str | Unset = UNSET
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
        if rule_id is not UNSET:
            field_dict["rule_id"] = rule_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        outcome = PermissionDecisionDeniedOutcome(d.pop("outcome"))

        scope = PermissionDecisionDeniedScope(d.pop("scope"))

        policy_version = d.pop("policy_version")

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_rule_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rule_id = _parse_rule_id(d.pop("rule_id", UNSET))

        permission_decision_denied = cls(
            outcome=outcome,
            scope=scope,
            policy_version=policy_version,
            reason=reason,
            rule_id=rule_id,
        )

        permission_decision_denied.additional_properties = d
        return permission_decision_denied

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
