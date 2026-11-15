# Generate typed adapters

Use this guide to generate Python clients and native handlers for a Harn source
contract. Install `harn-sdk` in a virtual environment and use a Harn executable
that provides `harn codegen generate`.

## Generate a module

```bash
harn-codegen-python \
  --file path/to/server.harn \
  --surface exports \
  --role both \
  --out generated
```

The launcher declares read access to its Python interpreter and SDK installation
roots. This also supports virtual environments backed by a separate managed
interpreter. Use `--plugin-read-root` for additional dependency installations.
Keep source files and credentials outside those roots. Harn denies
the backend access to contract source files and owns compilation, digest
validation, two-invocation determinism checks, and atomic artifact publication.
Pass `--ir contract.json` to require all three digests to match a frozen IR.
Use `--harn /path/to/harn` to select an explicit executable.

Choose `client`, `server`, or `both`. Repeated `--select` options select exact
operation names. Use `--surface script` for a script-published registry.

Run the same command with `--check` to detect drift without changing output.
A refusal writes a closed diagnostic to stderr and exits nonzero. Unsupported
wire types include their operation, type identity, and source reference.

## Call Harn

The checked-in [generated module](../examples/generated/pathological.py) comes
from Harn's shared recursive fixture. Its `Client` and `AsyncClient` accept the
existing `HarnClient` and `AsyncHarnClient`, preserving their credential policy.

```python
from pydantic import TypeAdapter
from harn import HarnClient
from harn.bindings import parse_wire_json
from examples.generated.pathological import Client, EchoInput

arguments = parse_wire_json(TypeAdapter(EchoInput), open("arguments.json").read())
with HarnClient(base_url="http://127.0.0.1:8080") as transport:
    result = Client(transport).echo(arguments)
```

The wire input is `{"input": ...}`. The shared payload is retained in
[`tests/fixtures/codegen/pathological/input.json`](../tests/fixtures/codegen/pathological/input.json).
Validate raw JSON with `parse_wire_json` so numeric token kinds, wire bytes,
decimal strings, and tuple arrays use their codecs. Native constructors accept `bytes`,
`Decimal`, tuples, and immutable `WireSet` values. Integers remain Python integers
with Harn's bounds enforced. `MISSING` distinguishes an omitted optional field
from an explicit nullable value.

Direct results and server-selected tasks use the same typed method. A declared
application failure returns `ApplicationFailure[DeclaredError]`; transport,
protocol, and runtime faults raise SDK errors. Cancel an async call normally.
The HTTP client accepts JSON and event-stream responses, reads the first RPC
response, and closes that response stream before collecting a separate task.
The client closes a direct HTTP exchange or requests cancellation of a known
Harn task. Task cancellation acknowledgment does not prove handler cleanup.

## Serve native handlers

Implement every generated operation once using either `SyncHandlers` or
`AsyncHandlers`. Each slot has its own typed callable protocol. Static checking
rejects missing or extra entries and wrong input, output, or async signatures;
registration also checks the exact census and sync/async kind before serving.

```python
from examples.native_generated import handlers
from examples.generated.pathological import create_async_server

create_async_server(handlers, max_concurrency=2).run_stdio()
```

The server uses the official MCP library for request dispatch and cancellation.
Each instance carries the three contract digests and forwards Harn's complete
tool catalog unchanged. Async handlers receive normal coroutine cancellation;
release resources in `finally`. Blocking sync handlers run in worker threads
and must finish before their thread is reclaimed.

Return an ordinary generated output value or an explicit `ApplicationFailure`.
Unexpected exceptions become value-free runtime faults. Input and output are
revalidated before a success is published, including values constructed without
Pydantic validation. Standard output belongs to the protocol; handler prints are
diverted to stderr while the server owns the streams.

Run one stdio service per worker process. The SDK pins MCP 2.3.0 because its
raw standard-stream claim API is private. A version and signature check refuses
an incompatible API before changing descriptors; upgrading that pin requires
the ownership, framing, cancellation, and EOF controls to pass again.

## Run the FastAPI example

[`examples/fastapi_generated.py`](../examples/fastapi_generated.py) exposes
`/echo-sync`, `/echo-async`, and `/scheduled` through real MCP calls. Start Harn
with the retained source fixture, then pass its base URL to `create_app`:

```bash
harn serve mcp --surface exports --transport http --bind 127.0.0.1:8080 \
  tests/fixtures/codegen/pathological/server.harn
```

```python
import uvicorn
from examples.fastapi_generated import create_app

uvicorn.run(create_app("http://127.0.0.1:8080"), host="127.0.0.1", port=3000)
```

Send `{"input": <shared payload>}` to any route. The example validates raw request
bytes before dispatch and returns the exact wire representation. Invalid input
returns HTTP 422 before calling Harn.

## Verify the installed wheel

CI installs the released runtime pinned in [`.harn-version`](../.harn-version)
after installing the built SDK wheel. To run its product check locally, install
the wheel into a virtual environment and run:

```bash
python scripts/check_codegen_product.py --harn "$(command -v harn)" --receipt codegen-product.json
```

The check refuses an SDK imported from the source tree or a missing runtime.
It exercises generation, sync and async HTTP calls, tasks, FastAPI routes and
native handlers. The retained receipt records the runtime identity and terminal
result, including the known worker cleanup checks.
