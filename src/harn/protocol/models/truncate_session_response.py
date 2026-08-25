from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.truncate_session_response_object import TruncateSessionResponseObject

if TYPE_CHECKING:
    from ..models.session import Session


T = TypeVar("T", bound="TruncateSessionResponse")


@_attrs_define
class TruncateSessionResponse:
    """
    Attributes:
        object_ (TruncateSessionResponseObject):
        session_id (str):
        kept_turn_count (int):
        removed_turn_count (int):
        new_tip_turn_id (None | str):
        session (Session):
    """

    object_: TruncateSessionResponseObject
    session_id: str
    kept_turn_count: int
    removed_turn_count: int
    new_tip_turn_id: None | str
    session: Session
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        session_id = self.session_id

        kept_turn_count = self.kept_turn_count

        removed_turn_count = self.removed_turn_count

        new_tip_turn_id: None | str
        new_tip_turn_id = self.new_tip_turn_id

        session = self.session.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "session_id": session_id,
                "kept_turn_count": kept_turn_count,
                "removed_turn_count": removed_turn_count,
                "new_tip_turn_id": new_tip_turn_id,
                "session": session,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.session import Session

        d = dict(src_dict)
        object_ = TruncateSessionResponseObject(d.pop("object"))

        session_id = d.pop("session_id")

        kept_turn_count = d.pop("kept_turn_count")

        removed_turn_count = d.pop("removed_turn_count")

        def _parse_new_tip_turn_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        new_tip_turn_id = _parse_new_tip_turn_id(d.pop("new_tip_turn_id"))

        session = Session.from_dict(d.pop("session"))

        truncate_session_response = cls(
            object_=object_,
            session_id=session_id,
            kept_turn_count=kept_turn_count,
            removed_turn_count=removed_turn_count,
            new_tip_turn_id=new_tip_turn_id,
            session=session,
        )

        truncate_session_response.additional_properties = d
        return truncate_session_response

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
