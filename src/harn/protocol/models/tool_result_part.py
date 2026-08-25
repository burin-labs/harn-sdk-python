from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.part_visibility import PartVisibility
from ..models.tool_result_part_status import ToolResultPartStatus
from ..models.tool_result_part_type import ToolResultPartType

T = TypeVar("T", bound="ToolResultPart")


@_attrs_define
class ToolResultPart:
    """
    Attributes:
        type_ (ToolResultPartType):
        tool_call_id (str):
        output (Any): Any JSON value.
        status (ToolResultPartStatus):
        visibility (PartVisibility):
    """

    type_: ToolResultPartType
    tool_call_id: str
    output: Any
    status: ToolResultPartStatus
    visibility: PartVisibility
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        tool_call_id = self.tool_call_id

        output = self.output

        status = self.status.value

        visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "tool_call_id": tool_call_id,
                "output": output,
                "status": status,
                "visibility": visibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = ToolResultPartType(d.pop("type"))

        tool_call_id = d.pop("tool_call_id")

        output = d.pop("output")

        status = ToolResultPartStatus(d.pop("status"))

        visibility = PartVisibility(d.pop("visibility"))

        tool_result_part = cls(
            type_=type_,
            tool_call_id=tool_call_id,
            output=output,
            status=status,
            visibility=visibility,
        )

        tool_result_part.additional_properties = d
        return tool_result_part

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
