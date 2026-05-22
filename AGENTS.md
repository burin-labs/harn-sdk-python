# AGENTS.md

## Scope

These instructions apply to the whole repository.

## Repository shape

This repo is the Python SDK for the Harn Agents API.

- Runtime code lives in `src/harn/`.
- Tests live in `tests/`.
- Runnable examples live in `examples/`.
- Release helper scripts live in `scripts/`.

## Local setup

Use Python 3.11 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Install release-only tools when you need package checks:

```bash
pip install build twine
```

## Checks

Run the tightest useful check first, then broaden before a PR.

```bash
python scripts/check_version_sync.py
ruff format --check src tests scripts
ruff check src tests scripts
pytest -q
```

Before release or packaging changes, also run:

```bash
python -m build
python -m twine check dist/*
```

## Editing notes

- Keep docs plain: short sentences, sentence-case headings, no filler, no sales tone.
- Do not claim named client helpers exist unless they are in `_OPENAPI_ENDPOINTS`.
- When the API surface changes, update `src/harn/client.py`, `tests/test_client.py`, examples, and `README.md` together.
- Keep sync and async client behavior aligned.
- `pyproject.toml` and `src/harn/__init__.py` must carry the same version. Use `scripts/bump_version.py` and verify with `scripts/check_version_sync.py`.
- Preserve public discovery behavior: `/health`, `/version`, `/openapi.json`, `/v1`, and `/v1/agent-card` do not attach auth or protocol headers.

## Git hygiene

Work on an isolated `ksinder/` branch. Rebase on `origin/main` before opening a PR.
