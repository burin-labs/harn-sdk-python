from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_object import JsonObject
    from ..models.metadata import Metadata


T = TypeVar("T", bound="CreateWorkspaceRequest")


@_attrs_define
class CreateWorkspaceRequest:
    """
    Attributes:
        name (str):
        root (str):
        image (None | str | Unset):
        packages (list[str] | Unset):
        network_policy (JsonObject | Unset):
        sandbox_backend (None | str | Unset):
        metadata (Metadata | Unset):
    """

    name: str
    root: str
    image: None | str | Unset = UNSET
    packages: list[str] | Unset = UNSET
    network_policy: JsonObject | Unset = UNSET
    sandbox_backend: None | str | Unset = UNSET
    metadata: Metadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        root = self.root

        image: None | str | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        packages: list[str] | Unset = UNSET
        if not isinstance(self.packages, Unset):
            packages = self.packages

        network_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.network_policy, Unset):
            network_policy = self.network_policy.to_dict()

        sandbox_backend: None | str | Unset
        if isinstance(self.sandbox_backend, Unset):
            sandbox_backend = UNSET
        else:
            sandbox_backend = self.sandbox_backend

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "root": root,
            }
        )
        if image is not UNSET:
            field_dict["image"] = image
        if packages is not UNSET:
            field_dict["packages"] = packages
        if network_policy is not UNSET:
            field_dict["network_policy"] = network_policy
        if sandbox_backend is not UNSET:
            field_dict["sandbox_backend"] = sandbox_backend
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.json_object import JsonObject
        from ..models.metadata import Metadata

        d = dict(src_dict)
        name = d.pop("name")

        root = d.pop("root")

        def _parse_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        packages = cast(list[str], d.pop("packages", UNSET))

        _network_policy = d.pop("network_policy", UNSET)
        network_policy: JsonObject | Unset
        if isinstance(_network_policy, Unset):
            network_policy = UNSET
        else:
            network_policy = JsonObject.from_dict(_network_policy)

        def _parse_sandbox_backend(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sandbox_backend = _parse_sandbox_backend(d.pop("sandbox_backend", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        create_workspace_request = cls(
            name=name,
            root=root,
            image=image,
            packages=packages,
            network_policy=network_policy,
            sandbox_backend=sandbox_backend,
            metadata=metadata,
        )

        create_workspace_request.additional_properties = d
        return create_workspace_request

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
