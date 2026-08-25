from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.provider_catalog_schema import ProviderCatalogSchema
from ..models.provider_catalog_schema_version import ProviderCatalogSchemaVersion
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provider_catalog_aliases_item import ProviderCatalogAliasesItem
    from ..models.provider_catalog_families_item import ProviderCatalogFamiliesItem
    from ..models.provider_catalog_models_item import ProviderCatalogModelsItem
    from ..models.provider_catalog_providers_item import ProviderCatalogProvidersItem
    from ..models.provider_catalog_qc_defaults import ProviderCatalogQcDefaults
    from ..models.provider_catalog_routing_routes_item import (
        ProviderCatalogRoutingRoutesItem,
    )
    from ..models.provider_catalog_variants_item import ProviderCatalogVariantsItem


T = TypeVar("T", bound="ProviderCatalog")


@_attrs_define
class ProviderCatalog:
    """
    Attributes:
        schema_version (ProviderCatalogSchemaVersion):
        schema (ProviderCatalogSchema):
        generated_by (str):
        providers (list[ProviderCatalogProvidersItem]):
        models (list[ProviderCatalogModelsItem]):
        aliases (list[ProviderCatalogAliasesItem]):
        variants (list[ProviderCatalogVariantsItem]):
        families (list[ProviderCatalogFamiliesItem]):
        qc_defaults (ProviderCatalogQcDefaults):
        routing_routes (list[ProviderCatalogRoutingRoutesItem] | Unset):
    """

    schema_version: ProviderCatalogSchemaVersion
    schema: ProviderCatalogSchema
    generated_by: str
    providers: list[ProviderCatalogProvidersItem]
    models: list[ProviderCatalogModelsItem]
    aliases: list[ProviderCatalogAliasesItem]
    variants: list[ProviderCatalogVariantsItem]
    families: list[ProviderCatalogFamiliesItem]
    qc_defaults: ProviderCatalogQcDefaults
    routing_routes: list[ProviderCatalogRoutingRoutesItem] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version.value

        schema = self.schema.value

        generated_by = self.generated_by

        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.to_dict()
            providers.append(providers_item)

        models = []
        for models_item_data in self.models:
            models_item = models_item_data.to_dict()
            models.append(models_item)

        aliases = []
        for aliases_item_data in self.aliases:
            aliases_item = aliases_item_data.to_dict()
            aliases.append(aliases_item)

        variants = []
        for variants_item_data in self.variants:
            variants_item = variants_item_data.to_dict()
            variants.append(variants_item)

        families = []
        for families_item_data in self.families:
            families_item = families_item_data.to_dict()
            families.append(families_item)

        qc_defaults = self.qc_defaults.to_dict()

        routing_routes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.routing_routes, Unset):
            routing_routes = []
            for routing_routes_item_data in self.routing_routes:
                routing_routes_item = routing_routes_item_data.to_dict()
                routing_routes.append(routing_routes_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "schema_version": schema_version,
                "schema": schema,
                "generated_by": generated_by,
                "providers": providers,
                "models": models,
                "aliases": aliases,
                "variants": variants,
                "families": families,
                "qc_defaults": qc_defaults,
            }
        )
        if routing_routes is not UNSET:
            field_dict["routing_routes"] = routing_routes

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.provider_catalog_aliases_item import ProviderCatalogAliasesItem
        from ..models.provider_catalog_families_item import ProviderCatalogFamiliesItem
        from ..models.provider_catalog_models_item import ProviderCatalogModelsItem
        from ..models.provider_catalog_providers_item import (
            ProviderCatalogProvidersItem,
        )
        from ..models.provider_catalog_qc_defaults import ProviderCatalogQcDefaults
        from ..models.provider_catalog_routing_routes_item import (
            ProviderCatalogRoutingRoutesItem,
        )
        from ..models.provider_catalog_variants_item import ProviderCatalogVariantsItem

        d = dict(src_dict)
        schema_version = ProviderCatalogSchemaVersion(d.pop("schema_version"))

        schema = ProviderCatalogSchema(d.pop("schema"))

        generated_by = d.pop("generated_by")

        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = ProviderCatalogProvidersItem.from_dict(providers_item_data)

            providers.append(providers_item)

        models = []
        _models = d.pop("models")
        for models_item_data in _models:
            models_item = ProviderCatalogModelsItem.from_dict(models_item_data)

            models.append(models_item)

        aliases = []
        _aliases = d.pop("aliases")
        for aliases_item_data in _aliases:
            aliases_item = ProviderCatalogAliasesItem.from_dict(aliases_item_data)

            aliases.append(aliases_item)

        variants = []
        _variants = d.pop("variants")
        for variants_item_data in _variants:
            variants_item = ProviderCatalogVariantsItem.from_dict(variants_item_data)

            variants.append(variants_item)

        families = []
        _families = d.pop("families")
        for families_item_data in _families:
            families_item = ProviderCatalogFamiliesItem.from_dict(families_item_data)

            families.append(families_item)

        qc_defaults = ProviderCatalogQcDefaults.from_dict(d.pop("qc_defaults"))

        _routing_routes = d.pop("routing_routes", UNSET)
        routing_routes: list[ProviderCatalogRoutingRoutesItem] | Unset = UNSET
        if _routing_routes is not UNSET:
            routing_routes = []
            for routing_routes_item_data in _routing_routes:
                routing_routes_item = ProviderCatalogRoutingRoutesItem.from_dict(
                    routing_routes_item_data
                )

                routing_routes.append(routing_routes_item)

        provider_catalog = cls(
            schema_version=schema_version,
            schema=schema,
            generated_by=generated_by,
            providers=providers,
            models=models,
            aliases=aliases,
            variants=variants,
            families=families,
            qc_defaults=qc_defaults,
            routing_routes=routing_routes,
        )

        return provider_catalog
