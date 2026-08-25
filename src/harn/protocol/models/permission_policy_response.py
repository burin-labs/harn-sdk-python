from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.permission_policy_response_object import PermissionPolicyResponseObject

if TYPE_CHECKING:
    from ..models.permission_policy import PermissionPolicy


T = TypeVar("T", bound="PermissionPolicyResponse")


@_attrs_define
class PermissionPolicyResponse:
    """
    Attributes:
        object_ (PermissionPolicyResponseObject):
        version (str): Content-hashed policy version.
        policy (PermissionPolicy): Declared permission policy: read/write/exec globs, net host
            allowlist, llm provider list + optional cost ceiling,
            redaction patterns, escalation chain.
    """

    object_: PermissionPolicyResponseObject
    version: str
    policy: PermissionPolicy
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        version = self.version

        policy = self.policy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "version": version,
                "policy": policy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.permission_policy import PermissionPolicy

        d = dict(src_dict)
        object_ = PermissionPolicyResponseObject(d.pop("object"))

        version = d.pop("version")

        policy = PermissionPolicy.from_dict(d.pop("policy"))

        permission_policy_response = cls(
            object_=object_,
            version=version,
            policy=policy,
        )

        permission_policy_response.additional_properties = d
        return permission_policy_response

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
