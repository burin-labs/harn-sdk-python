from __future__ import annotations

import warnings
from urllib.parse import urlsplit

DEFAULT_BASE_URL = "https://api.harnlang.com"
_LOCAL_HTTP_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "[::1]"})


def validate_base_url(base_url: str) -> tuple[str, str]:
    """Return a normalized URL and host after applying Harn's HTTPS policy."""
    parts = urlsplit(base_url)
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    if not (scheme == "https" or scheme == "http" and host in _LOCAL_HTTP_HOSTS):
        raise ValueError(
            f"Harn base_url must use https:// (got {base_url!r}); "
            "http:// is only allowed for localhost/127.0.0.1"
        )
    if not host:
        raise ValueError(f"Harn base_url is missing a host: {base_url!r}")
    return base_url.rstrip("/"), host


def warn_for_authenticated_custom_base_url(
    base_url: str, *, authenticated: bool, stacklevel: int = 2
) -> None:
    if authenticated and base_url.rstrip("/") != DEFAULT_BASE_URL:
        warnings.warn(
            f"Harn base_url overridden to {base_url!r} while a token/credential "
            "is configured. Only use credentials issued for this host.",
            UserWarning,
            stacklevel=stacklevel,
        )
