from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.permission_check_response_object import PermissionCheckResponseObject

if TYPE_CHECKING:
    from ..models.permission_decision_denied import PermissionDecisionDenied
    from ..models.permission_decision_granted import PermissionDecisionGranted
    from ..models.permission_decision_suspend import PermissionDecisionSuspend


T = TypeVar("T", bound="PermissionCheckResponse")


@_attrs_define
class PermissionCheckResponse:
    """
    Attributes:
        object_ (PermissionCheckResponseObject):
        request_id (str):
        decision (PermissionDecisionDenied | PermissionDecisionGranted | PermissionDecisionSuspend):
    """

    object_: PermissionCheckResponseObject
    request_id: str
    decision: (
        PermissionDecisionDenied | PermissionDecisionGranted | PermissionDecisionSuspend
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.permission_decision_denied import PermissionDecisionDenied
        from ..models.permission_decision_granted import PermissionDecisionGranted

        object_ = self.object_.value

        request_id = self.request_id

        decision: dict[str, Any]
        if isinstance(self.decision, PermissionDecisionGranted) or isinstance(
            self.decision, PermissionDecisionDenied
        ):
            decision = self.decision.to_dict()
        else:
            decision = self.decision.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "request_id": request_id,
                "decision": decision,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.permission_decision_denied import PermissionDecisionDenied
        from ..models.permission_decision_granted import PermissionDecisionGranted
        from ..models.permission_decision_suspend import PermissionDecisionSuspend

        d = dict(src_dict)
        object_ = PermissionCheckResponseObject(d.pop("object"))

        request_id = d.pop("request_id")

        def _parse_decision(
            data: object,
        ) -> (
            PermissionDecisionDenied
            | PermissionDecisionGranted
            | PermissionDecisionSuspend
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                decision_type_0 = PermissionDecisionGranted.from_dict(data)

                return decision_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                decision_type_1 = PermissionDecisionDenied.from_dict(data)

                return decision_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            decision_type_2 = PermissionDecisionSuspend.from_dict(data)

            return decision_type_2

        decision = _parse_decision(d.pop("decision"))

        permission_check_response = cls(
            object_=object_,
            request_id=request_id,
            decision=decision,
        )

        permission_check_response.additional_properties = d
        return permission_check_response

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
