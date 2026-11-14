"""Version-bound adapter to the official SDK's one standard-stream claim owner."""

# The SDK has no public raw-stream claim API. Keep private coupling in this file.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import inspect
import sys
from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from importlib.metadata import version
from typing import BinaryIO

from mcp.server import stdio


def check_stdio_api() -> None:
    if version("mcp") != "2.3.0":
        raise RuntimeError("Unsupported MCP standard-stream ownership version")
    expected = {
        "_claim_fd": ("fd", "stream", "mode", "open_diversion"),
        "_open_stdin_diversion": (),
        "_open_stdout_diversion": (),
    }
    for name, parameters in expected.items():
        function = getattr(stdio, name, None)
        if (
            not callable(function)
            or tuple(inspect.signature(function).parameters) != parameters
        ):
            raise RuntimeError("Unsupported MCP standard-stream ownership API")


@contextmanager
def claim_stdio() -> Iterator[tuple[BinaryIO, BinaryIO]]:
    check_stdio_api()
    sys.stdout.flush()
    with ExitStack() as claims:
        reader, restore_input = stdio._claim_fd(
            0, sys.stdin, "rb", stdio._open_stdin_diversion
        )
        if restore_input is not None:
            claims.callback(restore_input)
        writer, restore_output = stdio._claim_fd(
            1, sys.stdout, "wb", stdio._open_stdout_diversion
        )
        if restore_output is not None:
            claims.callback(restore_output)
        if (
            restore_input is None
            or restore_output is None
            or min(reader.fileno(), writer.fileno()) <= 2
        ):
            raise RuntimeError("Cannot isolate MCP standard streams")
        # The SDK retains private descriptors so a canceled blocking read can
        # never observe a recycled descriptor. Do not close its buffers here.
        try:
            yield reader, writer
        finally:
            sys.stdout.flush()
