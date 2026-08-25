from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.permission_response_request_class_type_1 import (
    PermissionResponseRequestClassType1,
)
from ..models.permission_response_request_class_type_2_type_1 import (
    PermissionResponseRequestClassType2Type1,
)
from ..models.permission_response_request_class_type_3_type_1 import (
    PermissionResponseRequestClassType3Type1,
)
from ..models.permission_response_request_outcome import (
    PermissionResponseRequestOutcome,
)
from ..models.permission_response_request_scope_type_1 import (
    PermissionResponseRequestScopeType1,
)
from ..models.permission_response_request_scope_type_2_type_1 import (
    PermissionResponseRequestScopeType2Type1,
)
from ..models.permission_response_request_scope_type_3_type_1 import (
    PermissionResponseRequestScopeType3Type1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="PermissionResponseRequest")


@_attrs_define
class PermissionResponseRequest:
    """
    Attributes:
        approved (bool | Unset): Preferred boolean approval switch.
        outcome (PermissionResponseRequestOutcome | Unset): Compatibility outcome for clients that mirror ACP wording.
        answer (Any | Unset): Any JSON value.
        reviewer (None | str | Unset):
        reason (None | str | Unset):
        metadata (Metadata | Unset):
        scope (None | PermissionResponseRequestScopeType1 | PermissionResponseRequestScopeType2Type1 |
            PermissionResponseRequestScopeType3Type1 | Unset): When the approver wants the verdict remembered, the scope at
            which to apply it. Honored only when `remember` is true.
        expires_at (datetime.datetime | None | Unset): Optional auto-revoke timestamp for time-bound grants.
        remember (bool | None | Unset): When true and the response approves or denies, materializes a
            persistent rule keyed off `scope` + `action_pattern` +
            `target_pattern`.
        action_pattern (None | str | Unset): Glob pattern matched against future `PermissionRequest.action`.
        target_pattern (None | str | Unset): Glob pattern matched against future `PermissionRequest.target`.
        class_ (None | PermissionResponseRequestClassType1 | PermissionResponseRequestClassType2Type1 |
            PermissionResponseRequestClassType3Type1 | Unset):
    """

    approved: bool | Unset = UNSET
    outcome: PermissionResponseRequestOutcome | Unset = UNSET
    answer: Any | Unset = UNSET
    reviewer: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    scope: (
        None
        | PermissionResponseRequestScopeType1
        | PermissionResponseRequestScopeType2Type1
        | PermissionResponseRequestScopeType3Type1
        | Unset
    ) = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    remember: bool | None | Unset = UNSET
    action_pattern: None | str | Unset = UNSET
    target_pattern: None | str | Unset = UNSET
    class_: (
        None
        | PermissionResponseRequestClassType1
        | PermissionResponseRequestClassType2Type1
        | PermissionResponseRequestClassType3Type1
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        approved = self.approved

        outcome: str | Unset = UNSET
        if not isinstance(self.outcome, Unset):
            outcome = self.outcome.value

        answer = self.answer

        reviewer: None | str | Unset
        if isinstance(self.reviewer, Unset):
            reviewer = UNSET
        else:
            reviewer = self.reviewer

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        scope: None | str | Unset
        if isinstance(self.scope, Unset):
            scope = UNSET
        elif (
            isinstance(self.scope, PermissionResponseRequestScopeType1)
            or isinstance(self.scope, PermissionResponseRequestScopeType2Type1)
            or isinstance(self.scope, PermissionResponseRequestScopeType3Type1)
        ):
            scope = self.scope.value
        else:
            scope = self.scope

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        remember: bool | None | Unset
        if isinstance(self.remember, Unset):
            remember = UNSET
        else:
            remember = self.remember

        action_pattern: None | str | Unset
        if isinstance(self.action_pattern, Unset):
            action_pattern = UNSET
        else:
            action_pattern = self.action_pattern

        target_pattern: None | str | Unset
        if isinstance(self.target_pattern, Unset):
            target_pattern = UNSET
        else:
            target_pattern = self.target_pattern

        class_: None | str | Unset
        if isinstance(self.class_, Unset):
            class_ = UNSET
        elif (
            isinstance(self.class_, PermissionResponseRequestClassType1)
            or isinstance(self.class_, PermissionResponseRequestClassType2Type1)
            or isinstance(self.class_, PermissionResponseRequestClassType3Type1)
        ):
            class_ = self.class_.value
        else:
            class_ = self.class_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if approved is not UNSET:
            field_dict["approved"] = approved
        if outcome is not UNSET:
            field_dict["outcome"] = outcome
        if answer is not UNSET:
            field_dict["answer"] = answer
        if reviewer is not UNSET:
            field_dict["reviewer"] = reviewer
        if reason is not UNSET:
            field_dict["reason"] = reason
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if scope is not UNSET:
            field_dict["scope"] = scope
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if remember is not UNSET:
            field_dict["remember"] = remember
        if action_pattern is not UNSET:
            field_dict["action_pattern"] = action_pattern
        if target_pattern is not UNSET:
            field_dict["target_pattern"] = target_pattern
        if class_ is not UNSET:
            field_dict["class"] = class_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        approved = d.pop("approved", UNSET)

        _outcome = d.pop("outcome", UNSET)
        outcome: PermissionResponseRequestOutcome | Unset
        if isinstance(_outcome, Unset):
            outcome = UNSET
        else:
            outcome = PermissionResponseRequestOutcome(_outcome)

        answer = d.pop("answer", UNSET)

        def _parse_reviewer(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reviewer = _parse_reviewer(d.pop("reviewer", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        def _parse_scope(
            data: object,
        ) -> (
            None
            | PermissionResponseRequestScopeType1
            | PermissionResponseRequestScopeType2Type1
            | PermissionResponseRequestScopeType3Type1
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_1 = PermissionResponseRequestScopeType1(data)

                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_2_type_1 = PermissionResponseRequestScopeType2Type1(data)

                return scope_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_3_type_1 = PermissionResponseRequestScopeType3Type1(data)

                return scope_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | PermissionResponseRequestScopeType1
                | PermissionResponseRequestScopeType2Type1
                | PermissionResponseRequestScopeType3Type1
                | Unset,
                data,
            )

        scope = _parse_scope(d.pop("scope", UNSET))

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

        def _parse_remember(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        remember = _parse_remember(d.pop("remember", UNSET))

        def _parse_action_pattern(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        action_pattern = _parse_action_pattern(d.pop("action_pattern", UNSET))

        def _parse_target_pattern(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_pattern = _parse_target_pattern(d.pop("target_pattern", UNSET))

        def _parse_class_(
            data: object,
        ) -> (
            None
            | PermissionResponseRequestClassType1
            | PermissionResponseRequestClassType2Type1
            | PermissionResponseRequestClassType3Type1
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                class_type_1 = PermissionResponseRequestClassType1(data)

                return class_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                class_type_2_type_1 = PermissionResponseRequestClassType2Type1(data)

                return class_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                class_type_3_type_1 = PermissionResponseRequestClassType3Type1(data)

                return class_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | PermissionResponseRequestClassType1
                | PermissionResponseRequestClassType2Type1
                | PermissionResponseRequestClassType3Type1
                | Unset,
                data,
            )

        class_ = _parse_class_(d.pop("class", UNSET))

        permission_response_request = cls(
            approved=approved,
            outcome=outcome,
            answer=answer,
            reviewer=reviewer,
            reason=reason,
            metadata=metadata,
            scope=scope,
            expires_at=expires_at,
            remember=remember,
            action_pattern=action_pattern,
            target_pattern=target_pattern,
            class_=class_,
        )

        permission_response_request.additional_properties = d
        return permission_response_request

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
