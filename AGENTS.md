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
python -m pip install -e ".[dev]"
```

Install release-only tools when you need package checks:

```bash
python -m pip install build twine
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
- `pyproject.toml` and `src/harn/__init__.py` must carry the same version. Use
  `scripts/bump_version.py` and verify with `scripts/check_version_sync.py`.
- Preserve public discovery behavior: `/health`, `/version`, `/openapi.json`,
  `/v1`, and `/v1/agent-card` do not attach auth or protocol headers.

## Git hygiene

Work in an isolated worktree and branch. Rebase on `origin/main` before opening a PR.

<!-- BEGIN HARN SHARED AGENT CONTRACT: managed by harn-bump-fleet -->

## Ecosystem working agreement

- Pursue the ambitious product outcome; make the seams boring with small typed
  interfaces, explicit invariants, and deterministic projections.
- Give each behavior one semantic owner. Generate or parity-test other surfaces
  instead of maintaining competing implementations.
- Work autonomously inside approved scope. Pause for destructive, production,
  high-spend, ambiguous, or authority-expanding actions—not routine reversible work.
- Treat stop, wait, stand down, and pivot as control events for long-lived work.
- Match evidence to the claim. Use the smallest owning product-path check;
  add a falsifier for contested, load-bearing, or potentially vacuous claims.
  Record relevant controls, recovery, and blind spots without repeating proof.
- Evidence follows source and artifact identity, not the branch name. Reuse
  verified branch or merge-candidate evidence after landing when relevant code,
  build inputs, and dependencies are unchanged. Repeat affected checks only
  for a relevant change, observed failure, deployment, or packaging difference.
- "Ship" means integrated on owning main with terminal integration checks and
  applicable release or deployment checks complete. Confirm the landed change
  and merge result; do not rebuild or recapture screenshots solely for main.
- Ship a ready PR by adding the `ship` label when the repo has a Smart Ship
  caller (`.github/workflows/smart-ship.yml`); otherwise land through the merge
  queue with `gh pr merge --squash --auto`. Never `gh pr merge --admin`.
  Incidents use the org override labels `bypass-ci`, `bypass-merge-queue`, or
  `force-merge`.

<!-- END HARN SHARED AGENT CONTRACT -->
