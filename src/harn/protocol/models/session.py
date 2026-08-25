from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.session_object import SessionObject
from ..models.session_state import SessionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject
    from ..models.live_session_client import LiveSessionClient
    from ..models.metadata import Metadata
    from ..models.session_model_policy import SessionModelPolicy


T = TypeVar("T", bound="Session")


@_attrs_define
class Session:
    """
    Attributes:
        id (str):
        object_ (SessionObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        workspace_id (str):
        state (SessionState):
        transcript (JsonObject | str):
        persona_id (None | str | Unset):
        model_policy (SessionModelPolicy | Unset): Concrete default model route for a session. Explicit per-call route
            and
            reasoning options take precedence, followed by this session policy,
            persona/script policy, and ambient runtime defaults.
        root_session_id (None | str | Unset):
        parent_session_id (None | str | Unset):
        branch_id (None | str | Unset):
        last_event_id (None | str | Unset):
        live_clients (list[LiveSessionClient] | Unset):
        live_controller_id (None | str | Unset):
        summary (None | str | Unset):
        expires_at (datetime.datetime | None | Unset):
    """

    id: str
    object_: SessionObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    workspace_id: str
    state: SessionState
    transcript: JsonObject | str
    persona_id: None | str | Unset = UNSET
    model_policy: SessionModelPolicy | Unset = UNSET
    root_session_id: None | str | Unset = UNSET
    parent_session_id: None | str | Unset = UNSET
    branch_id: None | str | Unset = UNSET
    last_event_id: None | str | Unset = UNSET
    live_clients: list[LiveSessionClient] | Unset = UNSET
    live_controller_id: None | str | Unset = UNSET
    summary: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.json_object import JsonObject

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        workspace_id = self.workspace_id

        state = self.state.value

        transcript: dict[str, Any] | str
        if isinstance(self.transcript, JsonObject):
            transcript = self.transcript.to_dict()
        else:
            transcript = self.transcript

        persona_id: None | str | Unset
        if isinstance(self.persona_id, Unset):
            persona_id = UNSET
        else:
            persona_id = self.persona_id

        model_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.model_policy, Unset):
            model_policy = self.model_policy.to_dict()

        root_session_id: None | str | Unset
        if isinstance(self.root_session_id, Unset):
            root_session_id = UNSET
        else:
            root_session_id = self.root_session_id

        parent_session_id: None | str | Unset
        if isinstance(self.parent_session_id, Unset):
            parent_session_id = UNSET
        else:
            parent_session_id = self.parent_session_id

        branch_id: None | str | Unset
        if isinstance(self.branch_id, Unset):
            branch_id = UNSET
        else:
            branch_id = self.branch_id

        last_event_id: None | str | Unset
        if isinstance(self.last_event_id, Unset):
            last_event_id = UNSET
        else:
            last_event_id = self.last_event_id

        live_clients: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.live_clients, Unset):
            live_clients = []
            for live_clients_item_data in self.live_clients:
                live_clients_item = live_clients_item_data.to_dict()
                live_clients.append(live_clients_item)

        live_controller_id: None | str | Unset
        if isinstance(self.live_controller_id, Unset):
            live_controller_id = UNSET
        else:
            live_controller_id = self.live_controller_id

        summary: None | str | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "workspace_id": workspace_id,
                "state": state,
                "transcript": transcript,
            }
        )
        if persona_id is not UNSET:
            field_dict["persona_id"] = persona_id
        if model_policy is not UNSET:
            field_dict["model_policy"] = model_policy
        if root_session_id is not UNSET:
            field_dict["root_session_id"] = root_session_id
        if parent_session_id is not UNSET:
            field_dict["parent_session_id"] = parent_session_id
        if branch_id is not UNSET:
            field_dict["branch_id"] = branch_id
        if last_event_id is not UNSET:
            field_dict["last_event_id"] = last_event_id
        if live_clients is not UNSET:
            field_dict["live_clients"] = live_clients
        if live_controller_id is not UNSET:
            field_dict["live_controller_id"] = live_controller_id
        if summary is not UNSET:
            field_dict["summary"] = summary
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject
        from ..models.live_session_client import LiveSessionClient
        from ..models.metadata import Metadata
        from ..models.session_model_policy import SessionModelPolicy

        d = dict(src_dict)
        id = d.pop("id")

        object_ = SessionObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        workspace_id = d.pop("workspace_id")

        state = SessionState(d.pop("state"))

        def _parse_transcript(data: object) -> JsonObject | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                transcript_type_0 = JsonObject.from_dict(data)

                return transcript_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JsonObject | str, data)

        transcript = _parse_transcript(d.pop("transcript"))

        def _parse_persona_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        persona_id = _parse_persona_id(d.pop("persona_id", UNSET))

        _model_policy = d.pop("model_policy", UNSET)
        model_policy: SessionModelPolicy | Unset
        if isinstance(_model_policy, Unset):
            model_policy = UNSET
        else:
            model_policy = SessionModelPolicy.from_dict(_model_policy)

        def _parse_root_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        root_session_id = _parse_root_session_id(d.pop("root_session_id", UNSET))

        def _parse_parent_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_session_id = _parse_parent_session_id(d.pop("parent_session_id", UNSET))

        def _parse_branch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        branch_id = _parse_branch_id(d.pop("branch_id", UNSET))

        def _parse_last_event_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_event_id = _parse_last_event_id(d.pop("last_event_id", UNSET))

        _live_clients = d.pop("live_clients", UNSET)
        live_clients: list[LiveSessionClient] | Unset = UNSET
        if _live_clients is not UNSET:
            live_clients = []
            for live_clients_item_data in _live_clients:
                live_clients_item = LiveSessionClient.from_dict(live_clients_item_data)

                live_clients.append(live_clients_item)

        def _parse_live_controller_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        live_controller_id = _parse_live_controller_id(
            d.pop("live_controller_id", UNSET)
        )

        def _parse_summary(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        session = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            workspace_id=workspace_id,
            state=state,
            transcript=transcript,
            persona_id=persona_id,
            model_policy=model_policy,
            root_session_id=root_session_id,
            parent_session_id=parent_session_id,
            branch_id=branch_id,
            last_event_id=last_event_id,
            live_clients=live_clients,
            live_controller_id=live_controller_id,
            summary=summary,
            expires_at=expires_at,
        )

        session.additional_properties = d
        return session

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
