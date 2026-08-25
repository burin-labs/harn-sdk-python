from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.permission_decision_suspend_outcome import (
    PermissionDecisionSuspendOutcome,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionDecisionSuspend")


@_attrs_define
class PermissionDecisionSuspend:
    """
    Attributes:
        outcome (PermissionDecisionSuspendOutcome):
        policy_version (str):
        escalate_to (list[str]):
        reason (None | str | Unset):
    """

    outcome: PermissionDecisionSuspendOutcome
    policy_version: str
    escalate_to: list[str]
    reason: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        outcome = self.outcome.value

        policy_version = self.policy_version

        escalate_to = self.escalate_to

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "outcome": outcome,
                "policy_version": policy_version,
                "escalate_to": escalate_to,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        outcome = PermissionDecisionSuspendOutcome(d.pop("outcome"))

        policy_version = d.pop("policy_version")

        escalate_to = cast(list[str], d.pop("escalate_to"))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        permission_decision_suspend = cls(
            outcome=outcome,
            policy_version=policy_version,
            escalate_to=escalate_to,
            reason=reason,
        )

        permission_decision_suspend.additional_properties = d
        return permission_decision_suspend

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
