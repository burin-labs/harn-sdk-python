from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.session_model_policy_reasoning_effort import (
    SessionModelPolicyReasoningEffort,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionModelPolicy")


@_attrs_define
class SessionModelPolicy:
    """Concrete default model route for a session. Explicit per-call route and
    reasoning options take precedence, followed by this session policy,
    persona/script policy, and ambient runtime defaults.

        Attributes:
            provider (str): Registered concrete provider identifier.
            model (str): Provider-native model identifier.
            reasoning_effort (SessionModelPolicyReasoningEffort | Unset): Optional provider-portable reasoning effort.
    """

    provider: str
    model: str
    reasoning_effort: SessionModelPolicyReasoningEffort | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        model = self.model

        reasoning_effort: str | Unset = UNSET
        if not isinstance(self.reasoning_effort, Unset):
            reasoning_effort = self.reasoning_effort.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider": provider,
                "model": model,
            }
        )
        if reasoning_effort is not UNSET:
            field_dict["reasoning_effort"] = reasoning_effort

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        provider = d.pop("provider")

        model = d.pop("model")

        _reasoning_effort = d.pop("reasoning_effort", UNSET)
        reasoning_effort: SessionModelPolicyReasoningEffort | Unset
        if isinstance(_reasoning_effort, Unset):
            reasoning_effort = UNSET
        else:
            reasoning_effort = SessionModelPolicyReasoningEffort(_reasoning_effort)

        session_model_policy = cls(
            provider=provider,
            model=model,
            reasoning_effort=reasoning_effort,
        )

        return session_model_policy
