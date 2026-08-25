from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.attach_session_client_request_mode import AttachSessionClientRequestMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="AttachSessionClientRequest")


@_attrs_define
class AttachSessionClientRequest:
    """
    Attributes:
        client_id (str):
        mode (AttachSessionClientRequestMode | Unset):  Default: AttachSessionClientRequestMode.OBSERVER.
        takeover (bool | Unset):  Default: False.
        prompt_injection (bool | Unset): Defaults to true for controllers and false for observers.
        permission_routing (bool | Unset): Defaults to true for controllers and false for observers.
        metadata (Metadata | Unset):
    """

    client_id: str
    mode: AttachSessionClientRequestMode | Unset = (
        AttachSessionClientRequestMode.OBSERVER
    )
    takeover: bool | Unset = False
    prompt_injection: bool | Unset = UNSET
    permission_routing: bool | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        takeover = self.takeover

        prompt_injection = self.prompt_injection

        permission_routing = self.permission_routing

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_id": client_id,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if takeover is not UNSET:
            field_dict["takeover"] = takeover
        if prompt_injection is not UNSET:
            field_dict["prompt_injection"] = prompt_injection
        if permission_routing is not UNSET:
            field_dict["permission_routing"] = permission_routing
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        client_id = d.pop("client_id")

        _mode = d.pop("mode", UNSET)
        mode: AttachSessionClientRequestMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = AttachSessionClientRequestMode(_mode)

        takeover = d.pop("takeover", UNSET)

        prompt_injection = d.pop("prompt_injection", UNSET)

        permission_routing = d.pop("permission_routing", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        attach_session_client_request = cls(
            client_id=client_id,
            mode=mode,
            takeover=takeover,
            prompt_injection=prompt_injection,
            permission_routing=permission_routing,
            metadata=metadata,
        )

        attach_session_client_request.additional_properties = d
        return attach_session_client_request

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
