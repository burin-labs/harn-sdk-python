from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..models.receipt_object import ReceiptObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.receipt_verification import ReceiptVerification
    from ..models.receipt_wire_envelope import ReceiptWireEnvelope
    from ..models.resource_pointer import ResourcePointer


T = TypeVar("T", bound="Receipt")


@_attrs_define
class Receipt:
    """
    Attributes:
        id (str):
        object_ (ReceiptObject):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata (Metadata):
        subject (ResourcePointer):
        format_ (str):
        summary (str):
        issued_at (datetime.datetime):
        issuer (str):
        wire (ReceiptWireEnvelope | Unset): Placeholder OpenAPI projection of the v1 receipt-format envelope. The
            sibling receipt-format spec owns canonicalization, signatures, hash
            chains, and redaction. Receipt resources reference that envelope here
            through `$ref` so generated clients can carry the wire receipt without
            treating it as an untyped trace.
        verification (None | ReceiptVerification | Unset):
    """

    id: str
    object_: ReceiptObject
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata: Metadata
    subject: ResourcePointer
    format_: str
    summary: str
    issued_at: datetime.datetime
    issuer: str
    wire: ReceiptWireEnvelope | Unset = UNSET
    verification: None | ReceiptVerification | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.receipt_verification import ReceiptVerification

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        subject = self.subject.to_dict()

        format_ = self.format_

        summary = self.summary

        issued_at = self.issued_at.isoformat()

        issuer = self.issuer

        wire: dict[str, Any] | Unset = UNSET
        if not isinstance(self.wire, Unset):
            wire = self.wire.to_dict()

        verification: dict[str, Any] | None | Unset
        if isinstance(self.verification, Unset):
            verification = UNSET
        elif isinstance(self.verification, ReceiptVerification):
            verification = self.verification.to_dict()
        else:
            verification = self.verification

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "updated_at": updated_at,
                "metadata": metadata,
                "subject": subject,
                "format": format_,
                "summary": summary,
                "issued_at": issued_at,
                "issuer": issuer,
            }
        )
        if wire is not UNSET:
            field_dict["wire"] = wire
        if verification is not UNSET:
            field_dict["verification"] = verification

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.metadata import Metadata
        from ..models.receipt_verification import ReceiptVerification
        from ..models.receipt_wire_envelope import ReceiptWireEnvelope
        from ..models.resource_pointer import ResourcePointer

        d = dict(src_dict)
        id = d.pop("id")

        object_ = ReceiptObject(d.pop("object"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        subject = ResourcePointer.from_dict(d.pop("subject"))

        format_ = d.pop("format")

        summary = d.pop("summary")

        issued_at = isoparse(d.pop("issued_at"))

        issuer = d.pop("issuer")

        _wire = d.pop("wire", UNSET)
        wire: ReceiptWireEnvelope | Unset
        if isinstance(_wire, Unset):
            wire = UNSET
        else:
            wire = ReceiptWireEnvelope.from_dict(_wire)

        def _parse_verification(data: object) -> None | ReceiptVerification | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_0 = ReceiptVerification.from_dict(data)

                return verification_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ReceiptVerification | Unset, data)

        verification = _parse_verification(d.pop("verification", UNSET))

        receipt = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            updated_at=updated_at,
            metadata=metadata,
            subject=subject,
            format_=format_,
            summary=summary,
            issued_at=issued_at,
            issuer=issuer,
            wire=wire,
            verification=verification,
        )

        receipt.additional_properties = d
        return receipt

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
