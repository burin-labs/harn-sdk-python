from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_signature import CardSignature
    from ..models.json_object import JsonObject
    from ..models.resource_pointer import ResourcePointer


T = TypeVar("T", bound="ReceiptWireEnvelope")


@_attrs_define
class ReceiptWireEnvelope:
    """Placeholder OpenAPI projection of the v1 receipt-format envelope. The
    sibling receipt-format spec owns canonicalization, signatures, hash
    chains, and redaction. Receipt resources reference that envelope here
    through `$ref` so generated clients can carry the wire receipt without
    treating it as an untyped trace.

        Attributes:
            schema_version (str):
            subject (ResourcePointer):
            issued_at (datetime.datetime):
            payload (JsonObject | Unset):
            signature (CardSignature | None | Unset):
    """

    schema_version: str
    subject: ResourcePointer
    issued_at: datetime.datetime
    payload: JsonObject | Unset = UNSET
    signature: CardSignature | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.card_signature import CardSignature

        schema_version = self.schema_version

        subject = self.subject.to_dict()

        issued_at = self.issued_at.isoformat()

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        signature: dict[str, Any] | None | Unset
        if isinstance(self.signature, Unset):
            signature = UNSET
        elif isinstance(self.signature, CardSignature):
            signature = self.signature.to_dict()
        else:
            signature = self.signature

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "subject": subject,
                "issued_at": issued_at,
            }
        )
        if payload is not UNSET:
            field_dict["payload"] = payload
        if signature is not UNSET:
            field_dict["signature"] = signature

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.card_signature import CardSignature
        from ..models.json_object import JsonObject
        from ..models.resource_pointer import ResourcePointer

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        subject = ResourcePointer.from_dict(d.pop("subject"))

        issued_at = isoparse(d.pop("issued_at"))

        _payload = d.pop("payload", UNSET)
        payload: JsonObject | Unset
        if isinstance(_payload, Unset):
            payload = UNSET
        else:
            payload = JsonObject.from_dict(_payload)

        def _parse_signature(data: object) -> CardSignature | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                signature_type_0 = CardSignature.from_dict(data)

                return signature_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CardSignature | None | Unset, data)

        signature = _parse_signature(d.pop("signature", UNSET))

        receipt_wire_envelope = cls(
            schema_version=schema_version,
            subject=subject,
            issued_at=issued_at,
            payload=payload,
            signature=signature,
        )

        receipt_wire_envelope.additional_properties = d
        return receipt_wire_envelope

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
