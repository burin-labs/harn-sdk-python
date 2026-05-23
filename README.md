# harn-sdk-python

Python SDK for the Harn Agents API.

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

The client sends `Authorization: Bearer ...` when a token is available. Token
lookup order is explicit `token`, then `credential`. As of the 2026-05-23
security sweep, the ambient `HARN_API_KEY` environment variable is **never**
read implicitly — pass `credential=AmbientCredential()` to opt in.

```python
from harn import AmbientCredential, HarnClient

# Explicit token
client = HarnClient(token="harn_live_...")

# Opt-in to $HARN_API_KEY (used to be automatic; now requires this line)
client = HarnClient(credential=AmbientCredential())
```

### Host-pinned bearer

The bearer token is bound to the host parsed from `base_url`. If a request URL
points at a different host (for example because you passed an absolute URL to
`client.request(...)`), the `Authorization` header is **not** attached. This
prevents a misconfigured `base_url` or a server-side redirect from leaking
the token cross-host. The constructor also raises `ValueError` for any
`base_url` whose scheme is not `https://` (with the single exception of
`http://localhost` and `http://127.0.0.1` for local development), and emits a
`UserWarning` when you override `base_url` while a token is configured.

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

`HARN_PROTOCOL_VERSION` is exported for callers that need to coordinate raw Harn
API requests. SDK v1 calls send
`Harn-Agents-Protocol-Version: agents-protocol-2026-04-25`; public discovery
helpers omit that header.

## API surface

`HarnClient` and `AsyncHarnClient` expose named helpers for the v1 OpenAPI
routes tracked in `src/harn/client.py`, including:

- public discovery
- runtime, capability, tool, and agent-card reads
- personas, workspaces, workspace files, sessions, messages, tasks, branches, and events
- permission requests, artifacts, receipts, memories, vaults, connectors, skills, outcomes, and quotas

Use `client.request(method, path, ...)` or `await client.request(...)` for API
routes that do not have a named helper yet.

## Streaming

Use SSE streaming helpers for task/session/global events:

```python
from harn import HarnClient

with HarnClient(base_url="http://localhost:8080") as client:
    for event in client.stream_task_events("task_123"):
        print(event.event, event.data)
```

### Streaming artifact downloads

For large artifacts (videos, models, datasets) use `stream_artifact_content`,
which yields chunks without buffering the body:

```python
with HarnClient(token="...") as client, open("video.mp4", "wb") as out:
    for chunk in client.stream_artifact_content("art_123"):
        out.write(chunk)
```

`download_artifact_content` is preserved for backwards compatibility but emits
a `DeprecationWarning` and loads the whole response into memory.

## Tool helper

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

Both clients include wrappers for endpoints defined in Harn OpenAPI.
Public discovery endpoints (`/health`, `/version`, `/openapi.json`, `/v1`, and
`/v1/agent-card`) do not attach auth or protocol headers. For experimental or
unwrapped endpoints, use `client.request(...)` or `await client.request(...)`.

Both clients share the same response handling: JSON responses return decoded
objects, `204` returns `None`, and error responses raise `ApiError`.

## Examples

See runnable examples in [`examples/`](examples):

- `01_invoke_workflow.py`: submit a workflow-shaped task
- `02_observe_transcript.py`: read session event streams
- `03_fire_trigger.py`: record trigger-like input
- `04_manage_session.py`: create, inspect, and close a session
- `05_deploy_pipeline.py`: publish pipeline metadata as artifacts and outcomes

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Release automation

### Workflows

- `CI` (`.github/workflows/ci.yml`)
  - checks version sync, formatting, lint, tests, build, and package metadata.
- `Publish` (`.github/workflows/publish.yml`)
  - publishes to PyPI on tags matching `v*` using Trusted Publishing (OIDC).
- `Release Bump` (`.github/workflows/release-bump.yml`)
  - bumps the version, commits to `main`, creates a tag, pushes, and creates a GitHub Release.

### Version management

Version is kept in:
- `pyproject.toml` (`[project].version`)
- `src/harn/__init__.py` (`__version__`)

Helpers:

```bash
python scripts/check_version_sync.py
python scripts/bump_version.py 0.1.0a1
```

### PyPI setup

PyPI creates the project on first successful upload when the package name is
available.

1. On PyPI, create a Trusted Publisher for this repository/workflow (`publish.yml`).
2. On GitHub, create an environment named `pypi` (optionally require reviewers).
3. Run the `Release Bump` workflow with a version like `0.1.0a1`.
4. The tag triggers `Publish`, which builds and uploads distributions.

If Trusted Publisher requires an existing project first, do a one-time bootstrap upload with a scoped API token, then switch fully to Trusted Publishing.

### Local fallback release

Use this only when the release workflow is unavailable.

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
