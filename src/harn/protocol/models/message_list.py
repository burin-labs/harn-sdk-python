from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.paginated_list_object import PaginatedListObject

if TYPE_CHECKING:
    from ..models.page_info import PageInfo
    from ..models.tool import Tool


T = TypeVar("T", bound="MessageList")


@_attrs_define
class MessageList:
    """
    Attributes:
        object_ (PaginatedListObject):
        data (list[Tool]):
        page (PageInfo):
    """

    object_: PaginatedListObject
    data: list[Tool]
    page: PageInfo
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        page = self.page.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "data": data,
                "page": page,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.page_info import PageInfo
        from ..models.tool import Tool

        d = dict(src_dict)
        object_ = PaginatedListObject(d.pop("object"))

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Tool.from_dict(data_item_data)

            data.append(data_item)

        page = PageInfo.from_dict(d.pop("page"))

        message_list = cls(
            object_=object_,
            data=data,
            page=page,
        )

        message_list.additional_properties = d
        return message_list

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
