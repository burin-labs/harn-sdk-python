from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission_policy_llm import PermissionPolicyLlm
    from ..models.permission_policy_redact import PermissionPolicyRedact


T = TypeVar("T", bound="PermissionPolicy")


@_attrs_define
class PermissionPolicy:
    """Declared permission policy: read/write/exec globs, net host
    allowlist, llm provider list + optional cost ceiling,
    redaction patterns, escalation chain.

        Attributes:
            read (list[str] | Unset):
            write (list[str] | Unset):
            exec_ (list[str] | Unset):
            net (list[str] | Unset):
            llm (PermissionPolicyLlm | Unset):
            redact (PermissionPolicyRedact | Unset):
            escalate_to (list[str] | Unset): Free-form identifiers tried in order (persona URI, the
                literal `user`, group name). The first online escalator
                receives the request.
    """

    read: list[str] | Unset = UNSET
    write: list[str] | Unset = UNSET
    exec_: list[str] | Unset = UNSET
    net: list[str] | Unset = UNSET
    llm: PermissionPolicyLlm | Unset = UNSET
    redact: PermissionPolicyRedact | Unset = UNSET
    escalate_to: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        read: list[str] | Unset = UNSET
        if not isinstance(self.read, Unset):
            read = self.read

        write: list[str] | Unset = UNSET
        if not isinstance(self.write, Unset):
            write = self.write

        exec_: list[str] | Unset = UNSET
        if not isinstance(self.exec_, Unset):
            exec_ = self.exec_

        net: list[str] | Unset = UNSET
        if not isinstance(self.net, Unset):
            net = self.net

        llm: dict[str, Any] | Unset = UNSET
        if not isinstance(self.llm, Unset):
            llm = self.llm.to_dict()

        redact: dict[str, Any] | Unset = UNSET
        if not isinstance(self.redact, Unset):
            redact = self.redact.to_dict()

        escalate_to: list[str] | Unset = UNSET
        if not isinstance(self.escalate_to, Unset):
            escalate_to = self.escalate_to

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if read is not UNSET:
            field_dict["read"] = read
        if write is not UNSET:
            field_dict["write"] = write
        if exec_ is not UNSET:
            field_dict["exec"] = exec_
        if net is not UNSET:
            field_dict["net"] = net
        if llm is not UNSET:
            field_dict["llm"] = llm
        if redact is not UNSET:
            field_dict["redact"] = redact
        if escalate_to is not UNSET:
            field_dict["escalate_to"] = escalate_to

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.permission_policy_llm import PermissionPolicyLlm
        from ..models.permission_policy_redact import PermissionPolicyRedact

        d = dict(src_dict)
        read = cast(list[str], d.pop("read", UNSET))

        write = cast(list[str], d.pop("write", UNSET))

        exec_ = cast(list[str], d.pop("exec", UNSET))

        net = cast(list[str], d.pop("net", UNSET))

        _llm = d.pop("llm", UNSET)
        llm: PermissionPolicyLlm | Unset
        if isinstance(_llm, Unset):
            llm = UNSET
        else:
            llm = PermissionPolicyLlm.from_dict(_llm)

        _redact = d.pop("redact", UNSET)
        redact: PermissionPolicyRedact | Unset
        if isinstance(_redact, Unset):
            redact = UNSET
        else:
            redact = PermissionPolicyRedact.from_dict(_redact)

        escalate_to = cast(list[str], d.pop("escalate_to", UNSET))

        permission_policy = cls(
            read=read,
            write=write,
            exec_=exec_,
            net=net,
            llm=llm,
            redact=redact,
            escalate_to=escalate_to,
        )

        permission_policy.additional_properties = d
        return permission_policy

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
