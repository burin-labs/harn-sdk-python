from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.live_session_client import LiveSessionClient


T = TypeVar("T", bound="LiveSessionClientChange")


@_attrs_define
class LiveSessionClientChange:
    """
    Attributes:
        client (LiveSessionClient | None):
        previous_controller_id (None | str):
        active_controller_id (None | str):
        clients (list[LiveSessionClient]):
    """

    client: LiveSessionClient | None
    previous_controller_id: None | str
    active_controller_id: None | str
    clients: list[LiveSessionClient]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.live_session_client import LiveSessionClient

        client: dict[str, Any] | None
        if isinstance(self.client, LiveSessionClient):
            client = self.client.to_dict()
        else:
            client = self.client

        previous_controller_id: None | str
        previous_controller_id = self.previous_controller_id

        active_controller_id: None | str
        active_controller_id = self.active_controller_id

        clients = []
        for clients_item_data in self.clients:
            clients_item = clients_item_data.to_dict()
            clients.append(clients_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client": client,
                "previous_controller_id": previous_controller_id,
                "active_controller_id": active_controller_id,
                "clients": clients,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.live_session_client import LiveSessionClient

        d = dict(src_dict)

        def _parse_client(data: object) -> LiveSessionClient | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                client_type_0 = LiveSessionClient.from_dict(data)

                return client_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LiveSessionClient | None, data)

        client = _parse_client(d.pop("client"))

        def _parse_previous_controller_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        previous_controller_id = _parse_previous_controller_id(
            d.pop("previous_controller_id")
        )

        def _parse_active_controller_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        active_controller_id = _parse_active_controller_id(
            d.pop("active_controller_id")
        )

        clients = []
        _clients = d.pop("clients")
        for clients_item_data in _clients:
            clients_item = LiveSessionClient.from_dict(clients_item_data)

            clients.append(clients_item)

        live_session_client_change = cls(
            client=client,
            previous_controller_id=previous_controller_id,
            active_controller_id=active_controller_id,
            clients=clients,
        )

        live_session_client_change.additional_properties = d
        return live_session_client_change

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
