"""Regenerate the Python example from the retained Harn-owned IR fixture."""

import argparse
from pathlib import Path

from harn._codegen.api import render
from harn._codegen.request import CodegenIr, CodegenRole

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    ir = CodegenIr.model_validate_json(
        (ROOT / "tests/fixtures/codegen/pathological/ir.json").read_bytes()
    )
    artifact = render(ir, CodegenRole.BOTH)
    target = ROOT / "examples/generated/pathological.py"
    if args.check:
        return 0 if target.is_file() and target.read_text() == artifact.content else 1
    target.write_text(artifact.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
