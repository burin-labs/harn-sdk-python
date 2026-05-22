from __future__ import annotations

import json
from typing import Iterator

from .models import StreamEvent


class SSEParser:
    def __init__(self) -> None:
        self.current_id: str | None = None
        self.current_event: str | None = None
        self.current_retry: int | None = None
        self.data_parts: list[str] = []

    def _flush(self) -> StreamEvent | None:
        if (
            self.current_id is None
            and self.current_event is None
            and not self.data_parts
        ):
            return None
        raw_data = "\n".join(self.data_parts) if self.data_parts else None
        parsed_data: object = raw_data
        if raw_data:
            try:
                parsed_data = json.loads(raw_data)
            except json.JSONDecodeError:
                parsed_data = raw_data
        event = StreamEvent(
            id=self.current_id,
            event=self.current_event,
            data=parsed_data,
            retry=self.current_retry,
        )
        self.current_id = None
        self.current_event = None
        self.current_retry = None
        self.data_parts = []
        return event

    def push(self, line: str) -> StreamEvent | None:
        if line == "":
            return self._flush()
        if line.startswith(":"):
            return None

        field, _, value = line.partition(":")
        value = value.lstrip(" ")
        if field == "id":
            self.current_id = value
        elif field == "event":
            self.current_event = value
        elif field == "retry":
            try:
                self.current_retry = int(value)
            except ValueError:
                pass
        elif field == "data":
            self.data_parts.append(value)
        return None

    def finish(self) -> StreamEvent | None:
        return self._flush()


def parse_sse_lines(lines: Iterator[str]) -> Iterator[StreamEvent]:
    parser = SSEParser()

    for raw in lines:
        line = raw.rstrip("\r\n")
        event = parser.push(line)
        if event is not None:
            yield event

    tail = parser.finish()
    if tail is not None:
        yield tail
