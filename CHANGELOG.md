# Changelog

All notable changes to `harn-sdk` are tracked here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
calendar-aligned alpha versions while pre-1.0.

## Unreleased

### Security

- **F1 (HIGH) — Cross-host bearer leak guard.** The `Authorization` header is
  now host-pinned to the configured `base_url`. Requests that resolve to a
  different host (typically because an absolute URL was passed to
  `client.request(...)`) no longer carry the bearer token. A `UserWarning` is
  emitted when `base_url` is overridden while a token is configured.
- **F2 (MEDIUM) — `AmbientCredential` is now opt-in.** `HarnClient` no longer
  silently falls back to `os.getenv("HARN_API_KEY")` when no token or
  credential is supplied. Pass `credential=AmbientCredential()` explicitly to
  preserve the old behaviour.
- **F9 (LOW) — `base_url` scheme allowlist.** Constructing the client with a
  non-https `base_url` now raises `ValueError` unless the host is `localhost`
  or `127.0.0.1`.

### Added

- **F8 (MEDIUM) — `stream_artifact_content`** on both `HarnClient` and
  `AsyncHarnClient` streams artifact bytes without buffering. Use it for
  videos, models, or any large payload.

### Deprecated

- `download_artifact_content` now emits a `DeprecationWarning` and remains
  only for backwards compatibility; switch callers to
  `stream_artifact_content` for any non-trivial payload.
