from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.task_object import TaskObject
from ..models.task_status import TaskStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.failure import Failure
    from ..models.json_object import JsonObject
    from ..models.message import Message
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Task")


@_attrs_define
class Task:
    """
    Attributes:
        id (str):
        object_ (TaskObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        session_id (str):
        workspace_id (str):
        status (TaskStatus):
        input_ (JsonObject | Message):
        created_by (str):
        persona_id (None | str | Unset):
        branch_id (None | str | Unset):
        parent_task_id (None | str | Unset): Source Task id for replay and delegated child Tasks, otherwise null.
        assigned_agent_id (None | str | Unset):
        receipt_id (None | str | Unset):
        outcome_id (None | str | Unset):
        quota_id (None | str | Unset):
        started_at (datetime.datetime | None | Unset):
        completed_at (datetime.datetime | None | Unset):
        canceled_at (datetime.datetime | None | Unset):
        failure (Failure | None | Unset):
    """

    id: str
    object_: TaskObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    session_id: str
    workspace_id: str
    status: TaskStatus
    input_: JsonObject | Message
    created_by: str
    persona_id: None | str | Unset = UNSET
    branch_id: None | str | Unset = UNSET
    parent_task_id: None | str | Unset = UNSET
    assigned_agent_id: None | str | Unset = UNSET
    receipt_id: None | str | Unset = UNSET
    outcome_id: None | str | Unset = UNSET
    quota_id: None | str | Unset = UNSET
    started_at: datetime.datetime | None | Unset = UNSET
    completed_at: datetime.datetime | None | Unset = UNSET
    canceled_at: datetime.datetime | None | Unset = UNSET
    failure: Failure | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.failure import Failure
        from ..models.message import Message

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        session_id = self.session_id

        workspace_id = self.workspace_id

        status = self.status.value

        input_: dict[str, Any]
        if isinstance(self.input_, Message):
            input_ = self.input_.to_dict()
        else:
            input_ = self.input_.to_dict()

        created_by = self.created_by

        persona_id: None | str | Unset
        if isinstance(self.persona_id, Unset):
            persona_id = UNSET
        else:
            persona_id = self.persona_id

        branch_id: None | str | Unset
        if isinstance(self.branch_id, Unset):
            branch_id = UNSET
        else:
            branch_id = self.branch_id

        parent_task_id: None | str | Unset
        if isinstance(self.parent_task_id, Unset):
            parent_task_id = UNSET
        else:
            parent_task_id = self.parent_task_id

        assigned_agent_id: None | str | Unset
        if isinstance(self.assigned_agent_id, Unset):
            assigned_agent_id = UNSET
        else:
            assigned_agent_id = self.assigned_agent_id

        receipt_id: None | str | Unset
        if isinstance(self.receipt_id, Unset):
            receipt_id = UNSET
        else:
            receipt_id = self.receipt_id

        outcome_id: None | str | Unset
        if isinstance(self.outcome_id, Unset):
            outcome_id = UNSET
        else:
            outcome_id = self.outcome_id

        quota_id: None | str | Unset
        if isinstance(self.quota_id, Unset):
            quota_id = UNSET
        else:
            quota_id = self.quota_id

        started_at: None | str | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        elif isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        canceled_at: None | str | Unset
        if isinstance(self.canceled_at, Unset):
            canceled_at = UNSET
        elif isinstance(self.canceled_at, datetime.datetime):
            canceled_at = self.canceled_at.isoformat()
        else:
            canceled_at = self.canceled_at

        failure: dict[str, Any] | None | Unset
        if isinstance(self.failure, Unset):
            failure = UNSET
        elif isinstance(self.failure, Failure):
            failure = self.failure.to_dict()
        else:
            failure = self.failure

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "session_id": session_id,
                "workspace_id": workspace_id,
                "status": status,
                "input": input_,
                "created_by": created_by,
            }
        )
        if persona_id is not UNSET:
            field_dict["persona_id"] = persona_id
        if branch_id is not UNSET:
            field_dict["branch_id"] = branch_id
        if parent_task_id is not UNSET:
            field_dict["parent_task_id"] = parent_task_id
        if assigned_agent_id is not UNSET:
            field_dict["assigned_agent_id"] = assigned_agent_id
        if receipt_id is not UNSET:
            field_dict["receipt_id"] = receipt_id
        if outcome_id is not UNSET:
            field_dict["outcome_id"] = outcome_id
        if quota_id is not UNSET:
            field_dict["quota_id"] = quota_id
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if canceled_at is not UNSET:
            field_dict["canceled_at"] = canceled_at
        if failure is not UNSET:
            field_dict["failure"] = failure

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.failure import Failure
        from ..models.json_object import JsonObject
        from ..models.message import Message
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = TaskObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        session_id = d.pop("session_id")

        workspace_id = d.pop("workspace_id")

        status = TaskStatus(d.pop("status"))

        def _parse_input_(data: object) -> JsonObject | Message:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_0 = Message.from_dict(data)

                return input_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            input_type_1 = JsonObject.from_dict(data)

            return input_type_1

        input_ = _parse_input_(d.pop("input"))

        created_by = d.pop("created_by")

        def _parse_persona_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        persona_id = _parse_persona_id(d.pop("persona_id", UNSET))

        def _parse_branch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        branch_id = _parse_branch_id(d.pop("branch_id", UNSET))

        def _parse_parent_task_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_task_id = _parse_parent_task_id(d.pop("parent_task_id", UNSET))

        def _parse_assigned_agent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        assigned_agent_id = _parse_assigned_agent_id(d.pop("assigned_agent_id", UNSET))

        def _parse_receipt_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        receipt_id = _parse_receipt_id(d.pop("receipt_id", UNSET))

        def _parse_outcome_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        outcome_id = _parse_outcome_id(d.pop("outcome_id", UNSET))

        def _parse_quota_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        quota_id = _parse_quota_id(d.pop("quota_id", UNSET))

        def _parse_started_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        started_at = _parse_started_at(d.pop("started_at", UNSET))

        def _parse_completed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        def _parse_canceled_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                canceled_at_type_0 = isoparse(data)

                return canceled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        canceled_at = _parse_canceled_at(d.pop("canceled_at", UNSET))

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

        task = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            session_id=session_id,
            workspace_id=workspace_id,
            status=status,
            input_=input_,
            created_by=created_by,
            persona_id=persona_id,
            branch_id=branch_id,
            parent_task_id=parent_task_id,
            assigned_agent_id=assigned_agent_id,
            receipt_id=receipt_id,
            outcome_id=outcome_id,
            quota_id=quota_id,
            started_at=started_at,
            completed_at=completed_at,
            canceled_at=canceled_at,
            failure=failure,
        )

        task.additional_properties = d
        return task

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
