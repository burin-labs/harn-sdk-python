from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.outcome_object import OutcomeObject
from ..models.outcome_status import OutcomeStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact import Artifact
    from ..models.failure import Failure
    from ..models.json_object import JsonObject
    from ..models.message import Message
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Outcome")


@_attrs_define
class Outcome:
    """
    Attributes:
        id (str):
        object_ (OutcomeObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        task_id (str):
        status (OutcomeStatus):
        summary (str):
        messages (list[Message] | Unset):
        artifacts (list[Artifact] | Unset):
        handoffs (list[JsonObject] | Unset):
        receipt_id (None | str | Unset):
        failure (Failure | None | Unset):
        cost (JsonObject | Unset):
        metrics (JsonObject | Unset):
    """

    id: str
    object_: OutcomeObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    task_id: str
    status: OutcomeStatus
    summary: str
    messages: list[Message] | Unset = UNSET
    artifacts: list[Artifact] | Unset = UNSET
    handoffs: list[JsonObject] | Unset = UNSET
    receipt_id: None | str | Unset = UNSET
    failure: Failure | None | Unset = UNSET
    cost: JsonObject | Unset = UNSET
    metrics: JsonObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.failure import Failure

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        task_id = self.task_id

        status = self.status.value

        summary = self.summary

        messages: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.messages, Unset):
            messages = []
            for messages_item_data in self.messages:
                messages_item = messages_item_data.to_dict()
                messages.append(messages_item)

        artifacts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.artifacts, Unset):
            artifacts = []
            for artifacts_item_data in self.artifacts:
                artifacts_item = artifacts_item_data.to_dict()
                artifacts.append(artifacts_item)

        handoffs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.handoffs, Unset):
            handoffs = []
            for handoffs_item_data in self.handoffs:
                handoffs_item = handoffs_item_data.to_dict()
                handoffs.append(handoffs_item)

        receipt_id: None | str | Unset
        if isinstance(self.receipt_id, Unset):
            receipt_id = UNSET
        else:
            receipt_id = self.receipt_id

        failure: dict[str, Any] | None | Unset
        if isinstance(self.failure, Unset):
            failure = UNSET
        elif isinstance(self.failure, Failure):
            failure = self.failure.to_dict()
        else:
            failure = self.failure

        cost: dict[str, Any] | Unset = UNSET
        if not isinstance(self.cost, Unset):
            cost = self.cost.to_dict()

        metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "task_id": task_id,
                "status": status,
                "summary": summary,
            }
        )
        if messages is not UNSET:
            field_dict["messages"] = messages
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts
        if handoffs is not UNSET:
            field_dict["handoffs"] = handoffs
        if receipt_id is not UNSET:
            field_dict["receipt_id"] = receipt_id
        if failure is not UNSET:
            field_dict["failure"] = failure
        if cost is not UNSET:
            field_dict["cost"] = cost
        if metrics is not UNSET:
            field_dict["metrics"] = metrics

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.artifact import Artifact
        from ..models.failure import Failure
        from ..models.json_object import JsonObject
        from ..models.message import Message
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = OutcomeObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        task_id = d.pop("task_id")

        status = OutcomeStatus(d.pop("status"))

        summary = d.pop("summary")

        _messages = d.pop("messages", UNSET)
        messages: list[Message] | Unset = UNSET
        if _messages is not UNSET:
            messages = []
            for messages_item_data in _messages:
                messages_item = Message.from_dict(messages_item_data)

                messages.append(messages_item)

        _artifacts = d.pop("artifacts", UNSET)
        artifacts: list[Artifact] | Unset = UNSET
        if _artifacts is not UNSET:
            artifacts = []
            for artifacts_item_data in _artifacts:
                artifacts_item = Artifact.from_dict(artifacts_item_data)

                artifacts.append(artifacts_item)

        _handoffs = d.pop("handoffs", UNSET)
        handoffs: list[JsonObject] | Unset = UNSET
        if _handoffs is not UNSET:
            handoffs = []
            for handoffs_item_data in _handoffs:
                handoffs_item = JsonObject.from_dict(handoffs_item_data)

                handoffs.append(handoffs_item)

        def _parse_receipt_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        receipt_id = _parse_receipt_id(d.pop("receipt_id", UNSET))

        def _parse_failure(data: object) -> Failure | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                failure_type_0 = Failure.from_dict(data)

                return failure_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Failure | None | Unset, data)

        failure = _parse_failure(d.pop("failure", UNSET))

        _cost = d.pop("cost", UNSET)
        cost: JsonObject | Unset
        if isinstance(_cost, Unset):
            cost = UNSET
        else:
            cost = JsonObject.from_dict(_cost)

        _metrics = d.pop("metrics", UNSET)
        metrics: JsonObject | Unset
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = JsonObject.from_dict(_metrics)

        outcome = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            task_id=task_id,
            status=status,
            summary=summary,
            messages=messages,
            artifacts=artifacts,
            handoffs=handoffs,
            receipt_id=receipt_id,
            failure=failure,
            cost=cost,
            metrics=metrics,
        )

        outcome.additional_properties = d
        return outcome

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
