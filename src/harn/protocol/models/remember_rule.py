from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.remember_rule_class import RememberRuleClass
from ..models.remember_rule_scope import RememberRuleScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="RememberRule")


@_attrs_define
class RememberRule:
    """
    Attributes:
        id (str): UUIDv7-prefixed rule identifier.
        scope (RememberRuleScope):
        class_ (RememberRuleClass):
        action_pattern (str):
        target_pattern (str):
        allow (bool):
        created_at (datetime.datetime):
        created_by (str):
        tenant_id (None | str | Unset):
        scope_value (None | str | Unset): Session id, workspace id, or actor, depending on scope.
        reason (None | str | Unset):
        expires_at (datetime.datetime | None | Unset):
        revoked_at (datetime.datetime | None | Unset):
    """

    id: str
    scope: RememberRuleScope
    class_: RememberRuleClass
    action_pattern: str
    target_pattern: str
    allow: bool
    created_at: datetime.datetime
    created_by: str
    tenant_id: None | str | Unset = UNSET
    scope_value: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    revoked_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        scope = self.scope.value

        class_ = self.class_.value

        action_pattern = self.action_pattern

        target_pattern = self.target_pattern

        allow = self.allow

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        tenant_id: None | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        else:
            tenant_id = self.tenant_id

        scope_value: None | str | Unset
        if isinstance(self.scope_value, Unset):
            scope_value = UNSET
        else:
            scope_value = self.scope_value

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

        revoked_at: None | str | Unset
        if isinstance(self.revoked_at, Unset):
            revoked_at = UNSET
        elif isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "scope": scope,
                "class": class_,
                "action_pattern": action_pattern,
                "target_pattern": target_pattern,
                "allow": allow,
                "created_at": created_at,
                "created_by": created_by,
            }
        )
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id
        if scope_value is not UNSET:
            field_dict["scope_value"] = scope_value
        if reason is not UNSET:
            field_dict["reason"] = reason
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if revoked_at is not UNSET:
            field_dict["revoked_at"] = revoked_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        scope = RememberRuleScope(d.pop("scope"))

        class_ = RememberRuleClass(d.pop("class"))

        action_pattern = d.pop("action_pattern")

        target_pattern = d.pop("target_pattern")

        allow = d.pop("allow")

        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        def _parse_tenant_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenant_id", UNSET))

        def _parse_scope_value(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scope_value = _parse_scope_value(d.pop("scope_value", UNSET))

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

        def _parse_revoked_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = isoparse(data)

                return revoked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        revoked_at = _parse_revoked_at(d.pop("revoked_at", UNSET))

        remember_rule = cls(
            id=id,
            scope=scope,
            class_=class_,
            action_pattern=action_pattern,
            target_pattern=target_pattern,
            allow=allow,
            created_at=created_at,
            created_by=created_by,
            tenant_id=tenant_id,
            scope_value=scope_value,
            reason=reason,
            expires_at=expires_at,
            revoked_at=revoked_at,
        )

        remember_rule.additional_properties = d
        return remember_rule

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
