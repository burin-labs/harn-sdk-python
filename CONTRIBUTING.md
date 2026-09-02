# Contributing to the Harn Python SDK

This guide is for anyone changing `harn-sdk`, the Python client for the Harn
Agents API. It covers setup, the checks to run, and how a release reaches PyPI.

The SDK is pre-1.0 and is not on PyPI yet, so its surface can still change
between versions. If you depend on it today, pin a commit.

## Set up a checkout

Use Python 3.11 or newer.

```bash
git clone https://github.com/burin-labs/harn-sdk-python.git
cd harn-sdk-python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

The editable install puts `src/harn/` on your path, so a change to the client
takes effect without reinstalling.

## Run the checks

Run the narrowest check that covers what you changed, then broaden before you
open a pull request.

```bash
python scripts/check_version_sync.py
ruff format --check src tests scripts
ruff check src tests scripts
pytest -q
```

`check_version_sync.py` fails when `pyproject.toml` and the package's declared
version disagree. That mismatch is the one release defect the tag-triggered
publish workflow cannot recover from, which is why it runs first.

If you touched packaging metadata, entry points, or anything under `scripts/`,
also build the distribution:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
python scripts/check_built_package.py
```

## Where the code comes from

Some of `src/harn/` is generated from the Harn protocol artifacts rather than
written by hand. `scripts/check_protocol_artifact.py` and
`scripts/normalize_protocol_artifact.py` own that path. When the Harn runtime
publishes new protocol artifacts, regenerate instead of hand-patching the
models: a hand-edit is erased at the next sync, and the mismatch shows up as a
decoding failure at runtime rather than as a failing test.

Hand-written code owns the client, the credential types, streaming, and the
webhook helpers. Those are the files to change for behavior.

## Security defaults you should not weaken

Three behaviors exist because of the 2026-05-23 security sweep. Changing any of
them needs a stated reason in the pull request:

- The bearer token is pinned to the host in `base_url`. A request that ends up
  at a different host does not carry `Authorization`.
- `base_url` must be `https://`, except `http://localhost` and
  `http://127.0.0.1`.
- `HARN_API_KEY` is never read implicitly. A caller opts in with
  `AmbientCredential()`.

Add a test alongside any change to these.

## Release and publish

1. Land the change on `main` with CI green.
2. Bump the version with `python scripts/bump_version.py`, and add the matching
   section to `CHANGELOG.md`.
3. Land the bump, then push the tag `vX.Y.Z`.

The tag starts the publish workflow, which re-checks that the tag matches the
package version, builds the distribution, and publishes through the `pypi`
environment using trusted publishing. Because the environment gates it, the
workflow waits rather than failing if the approval has not happened yet.

No version is on PyPI yet, so the first tag is also the first publish. Treat it
as such: check the built artifact locally with `twine check` before tagging.

## Pull request titles and descriptions

Title every pull request `[Area] Sentence case description`, for example
`[Client] Pin the bearer token to the base URL host`. Use one of `Client`,
`Protocol`, `Examples`, `Docs`, `CI`, `Tests`, or `Release`.

Keep the description to three to five sentences: what changed, why, the one
risk, and how you verified it. `.github/pull_request_template.md` carries the
prompts.

## Labels

`.github/labels.yml` records the label vocabulary. Priority, status, and effort
come from the org taxonomy in
[burin-labs/.github](https://github.com/burin-labs/.github); `area/*` is local
to this repository. Reuse `bug`, `enhancement`, and `documentation` for type
rather than adding a `type/*` prefix.

## Reporting a bug

Open an issue at
<https://github.com/burin-labs/harn-sdk-python/issues/new>. Include the SDK
commit, the Python version, and the request or stream that misbehaved. Never
paste a token, an API key, or a webhook signing secret into an issue.
