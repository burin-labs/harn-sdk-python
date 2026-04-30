# harn-sdk-python

Python SDK for the Harn Agents Protocol API.

## Install

```bash
pip install harn-sdk
```

## Quickstart

```python
from harn import HarnClient

with HarnClient(base_url="http://localhost:8080", token="...") as client:
    discovery = client.get_protocol_discovery()
    print(discovery)
```

## Authentication

The SDK supports:
- direct bearer token (`token="..."`)
- API key credential (`APIKeyCredential`)
- ambient credentials (`HARN_API_KEY`)
- OAuth2 device flow (`OAuthDeviceFlowCredential`)

## Streaming

Use SSE streaming helpers for task/session/global events:

```python
from harn import HarnClient

with HarnClient(base_url="http://localhost:8080") as client:
    for event in client.stream_task_events("task_123"):
        print(event.event, event.data)
```

## Tool Helper

```python
from harn import tool, registry

@tool(name="sum", description="Add two ints")
def sum_tool(a: int, b: int) -> int:
    return a + b

print([t.name for t in registry.list()])
```

## Clients

- `HarnClient`: synchronous API
- `AsyncHarnClient`: async API

Both clients include wrappers for the full v1 endpoints defined in Harn OpenAPI.

## Examples

See runnable examples in [`examples/`](examples):
- invoke a workflow/task
- observe transcript/event streams
- fire trigger-like input
- manage sessions
- deploy pipeline metadata

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## License

Apache-2.0
