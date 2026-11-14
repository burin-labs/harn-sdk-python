"""Expose typed sync, async, and server-selected task calls through FastAPI."""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import TypeAdapter

from harn import AsyncHarnClient, HarnClient
from harn.bindings import BindingError, parse_wire_json

from .generated.pathological import AsyncClient, Client, EchoInput


async def arguments(request: Request) -> EchoInput:
    try:
        # Validate raw JSON so bytes, decimals, and tuple arrays use wire codecs.
        return parse_wire_json(TypeAdapter(EchoInput), await request.body())
    except BindingError:
        raise HTTPException(422, "Invalid Harn wire arguments") from None


def create_app(base_url: str, *, token: str | None = None) -> FastAPI:
    app = FastAPI()

    @app.post("/echo-sync")
    def echo_sync(value: Annotated[EchoInput, Depends(arguments)]) -> JSONResponse:
        with HarnClient(base_url=base_url, token=token) as transport:
            result = Client(transport).echo(value)
        return JSONResponse(
            result.model_dump(mode="json", by_alias=True, exclude_unset=True)
        )

    @app.post("/echo-async")
    async def echo_async(
        value: Annotated[EchoInput, Depends(arguments)],
    ) -> JSONResponse:
        async with AsyncHarnClient(base_url=base_url, token=token) as transport:
            result = await AsyncClient(transport).echo(value)
        return JSONResponse(
            result.model_dump(mode="json", by_alias=True, exclude_unset=True)
        )

    @app.post("/scheduled")
    async def scheduled(
        value: Annotated[EchoInput, Depends(arguments)],
    ) -> JSONResponse:
        async with AsyncHarnClient(base_url=base_url, token=token) as transport:
            result = await AsyncClient(transport).scheduled(value)
        return JSONResponse(
            result.model_dump(mode="json", by_alias=True, exclude_unset=True)
        )

    return app
