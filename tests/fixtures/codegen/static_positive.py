from bindings import (
    AsyncClient,
    AsyncHandlers,
    Client,
    EchoInput,
    Payload,
    SyncHandlers,
    create_async_server,
    create_server,
)


def echo(arguments: EchoInput) -> Payload:
    return arguments.input


async def async_echo(arguments: EchoInput) -> Payload:
    return arguments.input


sync_handlers: SyncHandlers = {
    "echo": echo,
    "mutate": echo,
    "reject": echo,
    "scheduled": echo,
}
async_handlers: AsyncHandlers = {
    "echo": async_echo,
    "mutate": async_echo,
    "reject": async_echo,
    "scheduled": async_echo,
}
create_server(sync_handlers)
create_async_server(async_handlers)


def call(client: Client, value: EchoInput) -> Payload:
    return client.echo(value)


async def async_call(client: AsyncClient, value: EchoInput) -> Payload:
    return await client.echo(value)
