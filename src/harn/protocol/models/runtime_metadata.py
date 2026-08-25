from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.runtime_metadata_object import RuntimeMetadataObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.capability import Capability


T = TypeVar("T", bound="RuntimeMetadata")


@_attrs_define
class RuntimeMetadata:
    """
    Attributes:
        object_ (RuntimeMetadataObject):
        version (str):
        protocol_version (str):
        adapter (str):
        capabilities (list[Capability]):
        workspace_root (str | Unset):
        session_count (int | Unset):
        task_count (int | Unset):
    """

    object_: RuntimeMetadataObject
    version: str
    protocol_version: str
    adapter: str
    capabilities: list[Capability]
    workspace_root: str | Unset = UNSET
    session_count: int | Unset = UNSET
    task_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.value

        version = self.version

        protocol_version = self.protocol_version

        adapter = self.adapter

        capabilities = []
        for capabilities_item_data in self.capabilities:
            capabilities_item = capabilities_item_data.to_dict()
            capabilities.append(capabilities_item)

        workspace_root = self.workspace_root

        session_count = self.session_count

        task_count = self.task_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "version": version,
                "protocol_version": protocol_version,
                "adapter": adapter,
                "capabilities": capabilities,
            }
        )
        if workspace_root is not UNSET:
            field_dict["workspace_root"] = workspace_root
        if session_count is not UNSET:
            field_dict["session_count"] = session_count
        if task_count is not UNSET:
            field_dict["task_count"] = task_count

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.capability import Capability

        d = dict(src_dict)
        object_ = RuntimeMetadataObject(d.pop("object"))

        version = d.pop("version")

        protocol_version = d.pop("protocol_version")

        adapter = d.pop("adapter")

        capabilities = []
        _capabilities = d.pop("capabilities")
        for capabilities_item_data in _capabilities:
            capabilities_item = Capability.from_dict(capabilities_item_data)

            capabilities.append(capabilities_item)

        workspace_root = d.pop("workspace_root", UNSET)

        session_count = d.pop("session_count", UNSET)

        task_count = d.pop("task_count", UNSET)

        runtime_metadata = cls(
            object_=object_,
            version=version,
            protocol_version=protocol_version,
            adapter=adapter,
            capabilities=capabilities,
            workspace_root=workspace_root,
            session_count=session_count,
            task_count=task_count,
        )

        runtime_metadata.additional_properties = d
        return runtime_metadata

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
