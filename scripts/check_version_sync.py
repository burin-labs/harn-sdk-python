#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

PYPROJECT = Path("pyproject.toml")
INIT = Path("src/harn/__init__.py")


def read_pyproject_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r"(?m)^version\s*=\s*\"([^\"]+)\"\s*$", text)
    if not match:
        raise RuntimeError("Could not find [project].version in pyproject.toml")
    return match.group(1)


def read_init_version() -> str:
    text = INIT.read_text(encoding="utf-8")
    match = re.search(r"(?m)^__version__\s*=\s*\"([^\"]+)\"\s*$", text)
    if not match:
        raise RuntimeError("Could not find __version__ in src/harn/__init__.py")
    return match.group(1)


def main() -> int:
    pyproject_version = read_pyproject_version()
    init_version = read_init_version()
    if pyproject_version != init_version:
        print(
            "Version mismatch:\n"
            f"- pyproject.toml: {pyproject_version}\n"
            f"- src/harn/__init__.py: {init_version}",
            file=sys.stderr,
        )
        return 1

    print(f"Version sync OK: {pyproject_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
