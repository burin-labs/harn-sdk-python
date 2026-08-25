from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionPolicyLlm")


@_attrs_define
class PermissionPolicyLlm:
    """
    Attributes:
        providers (list[str] | Unset):
        cost_ceiling_usd_cents (int | None | Unset):
    """

    providers: list[str] | Unset = UNSET
    cost_ceiling_usd_cents: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        providers: list[str] | Unset = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers

        cost_ceiling_usd_cents: int | None | Unset
        if isinstance(self.cost_ceiling_usd_cents, Unset):
            cost_ceiling_usd_cents = UNSET
        else:
            cost_ceiling_usd_cents = self.cost_ceiling_usd_cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if providers is not UNSET:
            field_dict["providers"] = providers
        if cost_ceiling_usd_cents is not UNSET:
            field_dict["cost_ceiling_usd_cents"] = cost_ceiling_usd_cents

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        providers = cast(list[str], d.pop("providers", UNSET))

        def _parse_cost_ceiling_usd_cents(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cost_ceiling_usd_cents = _parse_cost_ceiling_usd_cents(
            d.pop("cost_ceiling_usd_cents", UNSET)
        )

        permission_policy_llm = cls(
            providers=providers,
            cost_ceiling_usd_cents=cost_ceiling_usd_cents,
        )

        permission_policy_llm.additional_properties = d
        return permission_policy_llm

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
