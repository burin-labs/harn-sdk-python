from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.event_object import EventObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject
    from ..models.metadata import Metadata
    from ..models.replay_event_metadata import ReplayEventMetadata
    from ..models.resource_pointer import ResourcePointer


T = TypeVar("T", bound="Event")


@_attrs_define
class Event:
    """
    Attributes:
        id (str):
        object_ (EventObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        event (str):
        resource (ResourcePointer):
        sequence (int):
        payload (JsonObject):
        trace_id (None | str | Unset):
        span_id (None | str | Unset):
        session_id (None | str | Unset):
        task_id (None | str | Unset):
        workspace_id (None | str | Unset):
        actor (None | str | Unset):
        idempotency_key (None | str | Unset):
        previous_event_id (None | str | Unset):
        receipt_id (None | str | Unset):
        replayed (bool | Unset):  Default: False.
        replay (None | ReplayEventMetadata | Unset):
    """

    id: str
    object_: EventObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    event: str
    resource: ResourcePointer
    sequence: int
    payload: JsonObject
    trace_id: None | str | Unset = UNSET
    span_id: None | str | Unset = UNSET
    session_id: None | str | Unset = UNSET
    task_id: None | str | Unset = UNSET
    workspace_id: None | str | Unset = UNSET
    actor: None | str | Unset = UNSET
    idempotency_key: None | str | Unset = UNSET
    previous_event_id: None | str | Unset = UNSET
    receipt_id: None | str | Unset = UNSET
    replayed: bool | Unset = False
    replay: None | ReplayEventMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.replay_event_metadata import ReplayEventMetadata

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        event = self.event

        resource = self.resource.to_dict()

        sequence = self.sequence

        payload = self.payload.to_dict()

        trace_id: None | str | Unset
        if isinstance(self.trace_id, Unset):
            trace_id = UNSET
        else:
            trace_id = self.trace_id

        span_id: None | str | Unset
        if isinstance(self.span_id, Unset):
            span_id = UNSET
        else:
            span_id = self.span_id

        session_id: None | str | Unset
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        task_id: None | str | Unset
        if isinstance(self.task_id, Unset):
            task_id = UNSET
        else:
            task_id = self.task_id

        workspace_id: None | str | Unset
        if isinstance(self.workspace_id, Unset):
            workspace_id = UNSET
        else:
            workspace_id = self.workspace_id

        actor: None | str | Unset
        if isinstance(self.actor, Unset):
            actor = UNSET
        else:
            actor = self.actor

        idempotency_key: None | str | Unset
        if isinstance(self.idempotency_key, Unset):
            idempotency_key = UNSET
        else:
            idempotency_key = self.idempotency_key

        previous_event_id: None | str | Unset
        if isinstance(self.previous_event_id, Unset):
            previous_event_id = UNSET
        else:
            previous_event_id = self.previous_event_id

        receipt_id: None | str | Unset
        if isinstance(self.receipt_id, Unset):
            receipt_id = UNSET
        else:
            receipt_id = self.receipt_id

        replayed = self.replayed

        replay: dict[str, Any] | None | Unset
        if isinstance(self.replay, Unset):
            replay = UNSET
        elif isinstance(self.replay, ReplayEventMetadata):
            replay = self.replay.to_dict()
        else:
            replay = self.replay

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "event": event,
                "resource": resource,
                "sequence": sequence,
                "payload": payload,
            }
        )
        if trace_id is not UNSET:
            field_dict["trace_id"] = trace_id
        if span_id is not UNSET:
            field_dict["span_id"] = span_id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if actor is not UNSET:
            field_dict["actor"] = actor
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key
        if previous_event_id is not UNSET:
            field_dict["previous_event_id"] = previous_event_id
        if receipt_id is not UNSET:
            field_dict["receipt_id"] = receipt_id
        if replayed is not UNSET:
            field_dict["replayed"] = replayed
        if replay is not UNSET:
            field_dict["replay"] = replay

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject
        from ..models.metadata import Metadata
        from ..models.replay_event_metadata import ReplayEventMetadata
        from ..models.resource_pointer import ResourcePointer

        d = dict(src_dict)
        id = d.pop("id")

        object_ = EventObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        event = d.pop("event")

        resource = ResourcePointer.from_dict(d.pop("resource"))

        sequence = d.pop("sequence")

        payload = JsonObject.from_dict(d.pop("payload"))

        def _parse_trace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

        def _parse_span_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        span_id = _parse_span_id(d.pop("span_id", UNSET))

        def _parse_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_task_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        task_id = _parse_task_id(d.pop("task_id", UNSET))

        def _parse_workspace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        workspace_id = _parse_workspace_id(d.pop("workspace_id", UNSET))

        def _parse_actor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        actor = _parse_actor(d.pop("actor", UNSET))

        def _parse_idempotency_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        idempotency_key = _parse_idempotency_key(d.pop("idempotency_key", UNSET))

        def _parse_previous_event_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        previous_event_id = _parse_previous_event_id(d.pop("previous_event_id", UNSET))

        def _parse_receipt_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        receipt_id = _parse_receipt_id(d.pop("receipt_id", UNSET))

        replayed = d.pop("replayed", UNSET)

        def _parse_replay(data: object) -> None | ReplayEventMetadata | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                replay_type_0 = ReplayEventMetadata.from_dict(data)

                return replay_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ReplayEventMetadata | Unset, data)

        replay = _parse_replay(d.pop("replay", UNSET))

        event = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            event=event,
            resource=resource,
            sequence=sequence,
            payload=payload,
            trace_id=trace_id,
            span_id=span_id,
            session_id=session_id,
            task_id=task_id,
            workspace_id=workspace_id,
            actor=actor,
            idempotency_key=idempotency_key,
            previous_event_id=previous_event_id,
            receipt_id=receipt_id,
            replayed=replayed,
            replay=replay,
        )

        event.additional_properties = d
        return event

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
