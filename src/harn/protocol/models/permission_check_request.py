from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.permission_check_request_class import PermissionCheckRequestClass
from ..models.permission_check_request_risk_type_1 import (
    PermissionCheckRequestRiskType1,
)
from ..models.permission_check_request_risk_type_2_type_1 import (
    PermissionCheckRequestRiskType2Type1,
)
from ..models.permission_check_request_risk_type_3_type_1 import (
    PermissionCheckRequestRiskType3Type1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission_check_request_context import PermissionCheckRequestContext


T = TypeVar("T", bound="PermissionCheckRequest")


@_attrs_define
class PermissionCheckRequest:
    """
    Attributes:
        session_id (str):
        actor (str):
        class_ (PermissionCheckRequestClass):
        action (str):
        target (str):
        id (None | str | Unset):
        tenant_id (None | str | Unset):
        workspace_id (None | str | Unset):
        risk (None | PermissionCheckRequestRiskType1 | PermissionCheckRequestRiskType2Type1 |
            PermissionCheckRequestRiskType3Type1 | Unset):
        context (PermissionCheckRequestContext | Unset):
        reason (None | str | Unset):
        requested_at (datetime.datetime | Unset):
    """

    session_id: str
    actor: str
    class_: PermissionCheckRequestClass
    action: str
    target: str
    id: None | str | Unset = UNSET
    tenant_id: None | str | Unset = UNSET
    workspace_id: None | str | Unset = UNSET
    risk: (
        None
        | PermissionCheckRequestRiskType1
        | PermissionCheckRequestRiskType2Type1
        | PermissionCheckRequestRiskType3Type1
        | Unset
    ) = UNSET
    context: PermissionCheckRequestContext | Unset = UNSET
    reason: None | str | Unset = UNSET
    requested_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        actor = self.actor

        class_ = self.class_.value

        action = self.action

        target = self.target

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        tenant_id: None | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        else:
            tenant_id = self.tenant_id

        workspace_id: None | str | Unset
        if isinstance(self.workspace_id, Unset):
            workspace_id = UNSET
        else:
            workspace_id = self.workspace_id

        risk: None | str | Unset
        if isinstance(self.risk, Unset):
            risk = UNSET
        elif (
            isinstance(self.risk, PermissionCheckRequestRiskType1)
            or isinstance(self.risk, PermissionCheckRequestRiskType2Type1)
            or isinstance(self.risk, PermissionCheckRequestRiskType3Type1)
        ):
            risk = self.risk.value
        else:
            risk = self.risk

        context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        requested_at: str | Unset = UNSET
        if not isinstance(self.requested_at, Unset):
            requested_at = self.requested_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "actor": actor,
                "class": class_,
                "action": action,
                "target": target,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if risk is not UNSET:
            field_dict["risk"] = risk
        if context is not UNSET:
            field_dict["context"] = context
        if reason is not UNSET:
            field_dict["reason"] = reason
        if requested_at is not UNSET:
            field_dict["requested_at"] = requested_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.permission_check_request_context import (
            PermissionCheckRequestContext,
        )

        d = dict(src_dict)
        session_id = d.pop("session_id")

        actor = d.pop("actor")

        class_ = PermissionCheckRequestClass(d.pop("class"))

        action = d.pop("action")

        target = d.pop("target")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_tenant_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenant_id", UNSET))

        def _parse_workspace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        workspace_id = _parse_workspace_id(d.pop("workspace_id", UNSET))

        def _parse_risk(
            data: object,
        ) -> (
            None
            | PermissionCheckRequestRiskType1
            | PermissionCheckRequestRiskType2Type1
            | PermissionCheckRequestRiskType3Type1
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                risk_type_1 = PermissionCheckRequestRiskType1(data)

                return risk_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                risk_type_2_type_1 = PermissionCheckRequestRiskType2Type1(data)

                return risk_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                risk_type_3_type_1 = PermissionCheckRequestRiskType3Type1(data)

                return risk_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | PermissionCheckRequestRiskType1
                | PermissionCheckRequestRiskType2Type1
                | PermissionCheckRequestRiskType3Type1
                | Unset,
                data,
            )

        risk = _parse_risk(d.pop("risk", UNSET))

        _context = d.pop("context", UNSET)
        context: PermissionCheckRequestContext | Unset
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = PermissionCheckRequestContext.from_dict(_context)

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        _requested_at = d.pop("requested_at", UNSET)
        requested_at: datetime.datetime | Unset
        if isinstance(_requested_at, Unset):
            requested_at = UNSET
        else:
            requested_at = isoparse(_requested_at)

        permission_check_request = cls(
            session_id=session_id,
            actor=actor,
            class_=class_,
            action=action,
            target=target,
            id=id,
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            risk=risk,
            context=context,
            reason=reason,
            requested_at=requested_at,
        )

        permission_check_request.additional_properties = d
        return permission_check_request

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
