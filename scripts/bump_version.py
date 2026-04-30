#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

PYPROJECT = Path("pyproject.toml")
INIT = Path("src/harn/__init__.py")


def replace_once(pattern: str, replacement: str, text: str, file_name: str) -> str:
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(
            f"Expected exactly one version field in {file_name}, found {count}"
        )
    return new_text


def bump(version: str) -> None:
    pyproject_text = PYPROJECT.read_text(encoding="utf-8")
    init_text = INIT.read_text(encoding="utf-8")

    pyproject_text = replace_once(
        r'^version\s*=\s*"[^\"]+"\s*$',
        f'version = "{version}"',
        pyproject_text,
        str(PYPROJECT),
    )
    init_text = replace_once(
        r'^__version__\s*=\s*"[^\"]+"\s*$',
        f'__version__ = "{version}"',
        init_text,
        str(INIT),
    )

    PYPROJECT.write_text(pyproject_text, encoding="utf-8")
    INIT.write_text(init_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bump package version in all tracked files."
    )
    parser.add_argument("version", help="New version, e.g. 0.1.0 or 0.1.0a1")
    args = parser.parse_args()

    bump(args.version)
    print(f"Updated version to {args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
