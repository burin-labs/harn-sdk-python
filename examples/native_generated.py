"""Run an exact typed native handler registry over ordinary MCP stdio."""

from harn.bindings import ApplicationFailure

from .generated.pathological import (
    AsyncHandlers,
    EchoInput,
    Failure,
    Failure_Rejected,
    Payload,
    create_async_server,
)


async def echo(arguments: EchoInput) -> Payload:
    return arguments.input


async def reject(_arguments: EchoInput) -> Payload | ApplicationFailure[Failure]:
    return ApplicationFailure(
        error=Failure_Rejected(
            enum_name="Failure", variant="Rejected", fields=("rejected",)
        )
    )


handlers: AsyncHandlers = {
    "echo": echo,
    "mutate": echo,
    "reject": reject,
    "scheduled": echo,
}

if __name__ == "__main__":
    create_async_server(handlers, max_concurrency=2).run_stdio()
