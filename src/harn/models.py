from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

JsonDict = dict[str, Any]


class HarnModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class Pagination(HarnModel):
    limit: int | None = None
    cursor: str | None = None
    next_cursor: str | None = Field(default=None, alias="nextCursor")


class ResourceList(HarnModel):
    items: list[JsonDict] = Field(default_factory=list)
    paging: Pagination | None = None


class ErrorBody(HarnModel):
    code: str
    message: str
    type: str | None = None
    param: str | None = None


class ApiError(Exception):
    def __init__(self, status_code: int, error: ErrorBody | None, body: Any) -> None:
        self.status_code = status_code
        self.error = error
        self.body = body
        detail = error.message if error else f"HTTP {status_code}"
        super().__init__(detail)


class StreamEvent(HarnModel):
    id: str | None = None
    event: str | None = None
    data: JsonDict | str | None = None
    retry: int | None = None
    received_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
