# fmt: off
from bindings import AsyncHandlers, Client, EchoInput, Payload, SyncHandlers

from harn.bindings import ApplicationFailure


def echo(arguments: EchoInput) -> Payload:
    return arguments.input


def wrong_input(arguments: str) -> Payload:
    raise ValueError(arguments)


def wrong_output(arguments: EchoInput) -> str:
    return str(arguments)


async def async_echo(arguments: EchoInput) -> Payload:
    return arguments.input


def wrong_error(_arguments: EchoInput) -> Payload | ApplicationFailure[str]:
    return ApplicationFailure(error="wrong declared error type")


missing: SyncHandlers = {"echo": echo}  # EXPECT reportAssignmentType
extra: SyncHandlers = {"echo": echo, "mutate": echo, "reject": echo, "scheduled": echo, "extra": echo}  # EXPECT reportAssignmentType
bad_input: SyncHandlers = {"echo": wrong_input, "mutate": echo, "reject": echo, "scheduled": echo}  # EXPECT reportAssignmentType
bad_output: SyncHandlers = {"echo": wrong_output, "mutate": echo, "reject": echo, "scheduled": echo}  # EXPECT reportAssignmentType
bad_sync: SyncHandlers = {"echo": async_echo, "mutate": echo, "reject": echo, "scheduled": echo}  # EXPECT reportAssignmentType
bad_async: AsyncHandlers = {"echo": echo, "mutate": async_echo, "reject": async_echo, "scheduled": async_echo}  # EXPECT reportAssignmentType
bad_error: SyncHandlers = {"echo": echo, "mutate": echo, "reject": wrong_error, "scheduled": echo}  # EXPECT reportAssignmentType


def call(client: Client) -> None:
    client.echo("wrong")  # EXPECT reportArgumentType


def input_model() -> EchoInput:
    return EchoInput(input="wrong")  # EXPECT reportArgumentType
