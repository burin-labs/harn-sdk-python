from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.session_model_policy import SessionModelPolicy


T = TypeVar("T", bound="UpdateSessionRequest")


@_attrs_define
class UpdateSessionRequest:
    """
    Attributes:
        summary (None | str | Unset):
        model_policy (None | SessionModelPolicy | Unset): Replaces the full session model policy; null clears it.
        metadata (Metadata | Unset):
    """

    summary: None | str | Unset = UNSET
    model_policy: None | SessionModelPolicy | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.session_model_policy import SessionModelPolicy

        summary: None | str | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        model_policy: dict[str, Any] | None | Unset
        if isinstance(self.model_policy, Unset):
            model_policy = UNSET
        elif isinstance(self.model_policy, SessionModelPolicy):
            model_policy = self.model_policy.to_dict()
        else:
            model_policy = self.model_policy

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if summary is not UNSET:
            field_dict["summary"] = summary
        if model_policy is not UNSET:
            field_dict["model_policy"] = model_policy
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata
        from ..models.session_model_policy import SessionModelPolicy

        d = dict(src_dict)

        def _parse_summary(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_model_policy(data: object) -> None | SessionModelPolicy | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_policy_type_0 = SessionModelPolicy.from_dict(data)

                return model_policy_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SessionModelPolicy | Unset, data)

        model_policy = _parse_model_policy(d.pop("model_policy", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        update_session_request = cls(
            summary=summary,
            model_policy=model_policy,
            metadata=metadata,
        )

        update_session_request.additional_properties = d
        return update_session_request

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
