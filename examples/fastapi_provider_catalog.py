from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException

from harn import ProtocolClient, create_harn_protocol_client
from harn.protocol.api.runtime import get_provider_catalog
from harn.protocol.models import ErrorResponse, ProviderCatalog


def load_provider_catalog(client: ProtocolClient) -> ProviderCatalog:
    result = get_provider_catalog.sync(client=client)
    if isinstance(result, ProviderCatalog):
        return result
    if isinstance(result, ErrorResponse):
        raise HTTPException(status_code=502, detail=result.to_dict())
    raise HTTPException(status_code=502, detail="Harn returned no provider catalog")


def create_app(client: ProtocolClient) -> FastAPI:
    app = FastAPI()

    @app.get("/models")
    def models() -> dict[str, object]:
        return load_provider_catalog(client).to_dict()

    return app


if __name__ == "__main__":
    import uvicorn

    harn = create_harn_protocol_client(
        base_url=os.getenv("HARN_BASE_URL", "https://api.harnlang.com"),
        token=os.getenv("HARN_ACCESS_TOKEN"),
    )
    uvicorn.run(create_app(harn), host="127.0.0.1", port=int(os.getenv("PORT", "3000")))
