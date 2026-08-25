from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_code import ErrorCode
from ..models.error_type import ErrorType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject


T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """
    Attributes:
        code (ErrorCode):
        message (str):
        type_ (ErrorType):
        param (None | str | Unset):
        request_id (None | str | Unset):
        details (JsonObject | Unset):
    """

    code: ErrorCode
    message: str
    type_: ErrorType
    param: None | str | Unset = UNSET
    request_id: None | str | Unset = UNSET
    details: JsonObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        type_ = self.type_.value

        param: None | str | Unset
        if isinstance(self.param, Unset):
            param = UNSET
        else:
            param = self.param

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        else:
            request_id = self.request_id

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "type": type_,
            }
        )
        if param is not UNSET:
            field_dict["param"] = param
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject

        d = dict(src_dict)
        code = ErrorCode(d.pop("code"))

        message = d.pop("message")

        type_ = ErrorType(d.pop("type"))

        def _parse_param(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        param = _parse_param(d.pop("param", UNSET))

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        _details = d.pop("details", UNSET)
        details: JsonObject | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = JsonObject.from_dict(_details)

        error = cls(
            code=code,
            message=message,
            type_=type_,
            param=param,
            request_id=request_id,
            details=details,
        )

        error.additional_properties = d
        return error

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
