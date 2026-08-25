from enum import Enum


class ProviderCatalogSchema(str, Enum):
    HTTPSHARNLANG_COMSCHEMASPROVIDER_CATALOG_V6_JSON = (
        "https://harnlang.com/schemas/provider-catalog.v6.json"
    )

    def __str__(self) -> str:
        return str(self.value)
