from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.permission_request_object import PermissionRequestObject
from ..models.permission_request_source import PermissionRequestSource
from ..models.permission_request_status import PermissionRequestStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="PermissionRequest")


@_attrs_define
class PermissionRequest:
    """
    Attributes:
        id (str):
        object_ (PermissionRequestObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        status (PermissionRequestStatus):
        source (PermissionRequestSource):
        request (Any): Any JSON value.
        session_id (None | str | Unset):
        task_id (None | str | Unset):
        action (Any | Unset): Any JSON value.
        response (Any | Unset): Any JSON value.
    """

    id: str
    object_: PermissionRequestObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    status: PermissionRequestStatus
    source: PermissionRequestSource
    request: Any
    session_id: None | str | Unset = UNSET
    task_id: None | str | Unset = UNSET
    action: Any | Unset = UNSET
    response: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        status = self.status.value

        source = self.source.value

        request = self.request

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

        action = self.action

        response = self.response

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "status": status,
                "source": source,
                "request": request,
            }
        )
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if action is not UNSET:
            field_dict["action"] = action
        if response is not UNSET:
            field_dict["response"] = response

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        object_ = PermissionRequestObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        status = PermissionRequestStatus(d.pop("status"))

        source = PermissionRequestSource(d.pop("source"))

        request = d.pop("request")

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

        action = d.pop("action", UNSET)

        response = d.pop("response", UNSET)

        permission_request = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            status=status,
            source=source,
            request=request,
            session_id=session_id,
            task_id=task_id,
            action=action,
            response=response,
        )

        permission_request.additional_properties = d
        return permission_request

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
