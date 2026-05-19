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
    session = client.create_session(body={"workspace_id": "wrk_123"})
    task = client.submit_session_task(
        session["id"],
        body={"input": {"role": "user", "parts": [{"type": "text", "text": "Ship it."}]}},
        idempotency_key="task-001",
    )

    for event in client.stream_task_events(task["id"]):
        print(event.event, event.data)
```

## Authentication

The client sends `Authorization: Bearer ...` when a token is available. Lookup
order is explicit `token`, then `credential`, then `HARN_API_KEY`.

```python
from harn import HarnClient

client = HarnClient(token="harn_live_...")
```

For OAuth device flow, call OIDC discovery when the issuer advertises custom
device and token endpoints:

```python
from harn import OAuthDeviceFlowCredential

credential = OAuthDeviceFlowCredential(
    "https://issuer.example",
    client_id="client-id",
    scope="tasks:create tasks:read",
)
credential.discover()
authorization = credential.start()
print(authorization["verification_uri"], authorization["user_code"])
credential.poll(authorization["device_code"])
```

`HARN_PROTOCOL_VERSION` is exported for callers that need to coordinate raw
requests with Harn Cloud. SDK v1 requests send
`Harn-Agents-Protocol-Version: agents-protocol-2026-04-25`; public discovery
helpers omit that header.

## Harn Cloud Surface

The client includes wrappers for the core v1 resources plus newer Cloud
surfaces used by current Harn releases:

- session and task suspend/resume
- lifecycle, pipeline, channel, and tool-call receipt audit reads
- context-pack creation, version approval/revocation, artifact review, and mount resolution
- persona cards, manifests, and schedule controls

Use `client.request(method, path, ...)` or `await client.request(...)` for
Cloud endpoints that do not have a named helper yet.

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

Both clients share the same response handling: JSON responses return decoded
objects, `204` returns `None`, and error responses raise `ApiError`.

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

## Release Automation

### Workflows

- `CI` (`.github/workflows/ci.yml`)
  - checks version sync, formatting, lint, tests, build, and package metadata validation.
- `Publish` (`.github/workflows/publish.yml`)
  - publishes to PyPI on tags matching `v*` using Trusted Publishing (OIDC).
- `Release Bump` (`.github/workflows/release-bump.yml`)
  - manual workflow to bump version, commit to `main`, create tag, push, and create GitHub Release.

### Version management

Version is kept in:
- `pyproject.toml` (`[project].version`)
- `src/harn/__init__.py` (`__version__`)

Helpers:

```bash
python scripts/check_version_sync.py
python scripts/bump_version.py 0.1.0a1
```

### PyPI setup (Trusted Publishing)

PyPI does not always expose a standalone "create project" button. The project is created on first successful upload when the package name is available.

Recommended setup:
1. On PyPI, create a Trusted Publisher for this repository/workflow (`publish.yml`).
2. On GitHub, create an environment named `pypi` (optionally require reviewers).
3. Run the `Release Bump` workflow with a version like `0.1.0a1`.
4. The tag triggers `Publish`, which builds and uploads distributions.

If Trusted Publisher requires an existing project first, do a one-time bootstrap upload with a scoped API token, then switch fully to Trusted Publishing.

### Local fallback release

```bash
git checkout main && git pull
python scripts/bump_version.py 0.1.0a1
python scripts/check_version_sync.py
git commit -am "release: v0.1.0a1"
git tag -a v0.1.0a1 -m "Release v0.1.0a1"
git push origin main --tags
```

## License

Apache-2.0
