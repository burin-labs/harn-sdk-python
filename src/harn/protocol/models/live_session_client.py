from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.live_session_client_mode import LiveSessionClientMode

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="LiveSessionClient")


@_attrs_define
class LiveSessionClient:
    """
    Attributes:
        client_id (str):
        mode (LiveSessionClientMode):
        attached_at (str): Runtime liveness marker for when the client first attached.
        last_seen_at (str): Runtime liveness marker refreshed by attach or heartbeat.
        prompt_injection (bool):
        permission_routing (bool):
        metadata (Metadata):
    """

    client_id: str
    mode: LiveSessionClientMode
    attached_at: str
    last_seen_at: str
    prompt_injection: bool
    permission_routing: bool
    metadata: Metadata
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        mode = self.mode.value

        attached_at = self.attached_at

        last_seen_at = self.last_seen_at

        prompt_injection = self.prompt_injection

        permission_routing = self.permission_routing

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_id": client_id,
                "mode": mode,
                "attached_at": attached_at,
                "last_seen_at": last_seen_at,
                "prompt_injection": prompt_injection,
                "permission_routing": permission_routing,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        client_id = d.pop("client_id")

        mode = LiveSessionClientMode(d.pop("mode"))

        attached_at = d.pop("attached_at")

        last_seen_at = d.pop("last_seen_at")

        prompt_injection = d.pop("prompt_injection")

        permission_routing = d.pop("permission_routing")

        metadata = Metadata.from_dict(d.pop("metadata"))

        live_session_client = cls(
            client_id=client_id,
            mode=mode,
            attached_at=attached_at,
            last_seen_at=last_seen_at,
            prompt_injection=prompt_injection,
            permission_routing=permission_routing,
            metadata=metadata,
        )

        live_session_client.additional_properties = d
        return live_session_client

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
