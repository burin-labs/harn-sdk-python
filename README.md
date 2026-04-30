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
