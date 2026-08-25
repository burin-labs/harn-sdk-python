from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.connector_object import ConnectorObject
from ..models.connector_status import ConnectorStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Connector")


@_attrs_define
class Connector:
    """
    Attributes:
        id (str):
        object_ (ConnectorObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        provider (str):
        workspace_id (str):
        status (ConnectorStatus):
        event_kinds (list[str]):
        dedupe_policy (JsonObject | Unset):
        auth (JsonObject | Unset):
        webhook (JsonObject | Unset):
        polling (JsonObject | Unset):
        target_persona_id (None | str | Unset):
        target_session_id (None | str | Unset):
    """

    id: str
    object_: ConnectorObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    provider: str
    workspace_id: str
    status: ConnectorStatus
    event_kinds: list[str]
    dedupe_policy: JsonObject | Unset = UNSET
    auth: JsonObject | Unset = UNSET
    webhook: JsonObject | Unset = UNSET
    polling: JsonObject | Unset = UNSET
    target_persona_id: None | str | Unset = UNSET
    target_session_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        provider = self.provider

        workspace_id = self.workspace_id

        status = self.status.value

        event_kinds = self.event_kinds

        dedupe_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dedupe_policy, Unset):
            dedupe_policy = self.dedupe_policy.to_dict()

        auth: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auth, Unset):
            auth = self.auth.to_dict()

        webhook: dict[str, Any] | Unset = UNSET
        if not isinstance(self.webhook, Unset):
            webhook = self.webhook.to_dict()

        polling: dict[str, Any] | Unset = UNSET
        if not isinstance(self.polling, Unset):
            polling = self.polling.to_dict()

        target_persona_id: None | str | Unset
        if isinstance(self.target_persona_id, Unset):
            target_persona_id = UNSET
        else:
            target_persona_id = self.target_persona_id

        target_session_id: None | str | Unset
        if isinstance(self.target_session_id, Unset):
            target_session_id = UNSET
        else:
            target_session_id = self.target_session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "provider": provider,
                "workspace_id": workspace_id,
                "status": status,
                "event_kinds": event_kinds,
            }
        )
        if dedupe_policy is not UNSET:
            field_dict["dedupe_policy"] = dedupe_policy
        if auth is not UNSET:
            field_dict["auth"] = auth
        if webhook is not UNSET:
            field_dict["webhook"] = webhook
        if polling is not UNSET:
            field_dict["polling"] = polling
        if target_persona_id is not UNSET:
            field_dict["target_persona_id"] = target_persona_id
        if target_session_id is not UNSET:
            field_dict["target_session_id"] = target_session_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = ConnectorObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        provider = d.pop("provider")

        workspace_id = d.pop("workspace_id")

        status = ConnectorStatus(d.pop("status"))

        event_kinds = cast(list[str], d.pop("event_kinds"))

        _dedupe_policy = d.pop("dedupe_policy", UNSET)
        dedupe_policy: JsonObject | Unset
        if isinstance(_dedupe_policy, Unset):
            dedupe_policy = UNSET
        else:
            dedupe_policy = JsonObject.from_dict(_dedupe_policy)

        _auth = d.pop("auth", UNSET)
        auth: JsonObject | Unset
        if isinstance(_auth, Unset):
            auth = UNSET
        else:
            auth = JsonObject.from_dict(_auth)

        _webhook = d.pop("webhook", UNSET)
        webhook: JsonObject | Unset
        if isinstance(_webhook, Unset):
            webhook = UNSET
        else:
            webhook = JsonObject.from_dict(_webhook)

        _polling = d.pop("polling", UNSET)
        polling: JsonObject | Unset
        if isinstance(_polling, Unset):
            polling = UNSET
        else:
            polling = JsonObject.from_dict(_polling)

        def _parse_target_persona_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_persona_id = _parse_target_persona_id(d.pop("target_persona_id", UNSET))

        def _parse_target_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_session_id = _parse_target_session_id(d.pop("target_session_id", UNSET))

        connector = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            provider=provider,
            workspace_id=workspace_id,
            status=status,
            event_kinds=event_kinds,
            dedupe_policy=dedupe_policy,
            auth=auth,
            webhook=webhook,
            polling=polling,
            target_persona_id=target_persona_id,
            target_session_id=target_session_id,
        )

        connector.additional_properties = d
        return connector

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
