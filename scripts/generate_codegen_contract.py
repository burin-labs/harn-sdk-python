"""Project Harn's vendored codegen schemas into closed Pydantic boundary records."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "src/harn/_codegen"


def protocol_value(value: object) -> bool:
    if value is None or type(value) in (str, int, bool):
        return True
    if isinstance(value, list):
        return all(protocol_value(item) for item in value)
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and protocol_value(item) for key, item in value.items()
        )
    return False


def protocol_literal(value: object) -> str:
    if isinstance(value, dict):
        fields = ", ".join(
            f"{key!r}: {protocol_literal(item)}" for key, item in sorted(value.items())
        )
        return "MappingProxyType({" + fields + "})"
    if isinstance(value, list):
        return "(" + "".join(protocol_literal(item) + "," for item in value) + ")"
    return repr(value)


def format_code(content: str, target: Path) -> str:
    checked = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--fix",
            "--stdin-filename",
            str(target),
            "-",
        ],
        input=content,
        text=True,
        capture_output=True,
        check=True,
        cwd=ROOT,
    ).stdout
    return subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--stdin-filename", str(target), "-"],
        input=checked,
        text=True,
        capture_output=True,
        check=True,
        cwd=ROOT,
    ).stdout


def project(name: str, class_name: str) -> str:
    with tempfile.TemporaryDirectory(prefix="harn-python-ir-") as directory:
        output = Path(directory) / "contract.py"
        command = [
            sys.executable,
            "-m",
            "datamodel_code_generator",
            "--input",
            str(CONTRACT / "schemas" / f"{name}-v1.json"),
            "--input-file-type",
            "jsonschema",
            "--output-model-type",
            "pydantic_v2.BaseModel",
            "--class-name",
            class_name,
            "--target-python-version",
            "3.11",
            "--disable-timestamp",
            "--use-standard-collections",
            "--use-union-operator",
            "--enum-field-as-literal",
            "none",
            "--capitalise-enum-members",
            "--deserialize-default-values",
            "enum",
            "--strict-types",
            "str",
            "bytes",
            "int",
            "float",
            "bool",
            "--extra-fields",
            "forbid",
            "--strict-refs",
            "--untrusted-input",
            "--strict-nullable",
            "--collapse-root-models",
            "--use-type-alias",
            "--field-constraints",
            "--use-annotated",
            "--type-overrides",
            '{"CodegenIr.mcp_tools":"harn._codegen.opaque.JsonArray"}',
            "--type-overrides-replace-whole-type",
            "--no-formatters",
            "--output",
            str(output),
        ]
        subprocess.run(command, check=True, cwd=ROOT)
        return format_code(output.read_text(), CONTRACT / f"{name}.py")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    different = []
    protocol = json.loads((CONTRACT / "schemas/protocol-v1.json").read_text())
    if (
        not isinstance(protocol, dict)
        or not protocol
        or not all(
            isinstance(key, str)
            and key.isidentifier()
            and key.isupper()
            and protocol_value(value)
            and (not isinstance(value, str) or bool(value))
            for key, value in protocol.items()
        )
    ):
        raise ValueError("invalid Harn codegen protocol projection")
    protocol_content = (
        "# Generated from Harn harn-codegen-protocol.json. Do not edit.\n"
        + "from typing import Final\n"
        + (
            "from collections.abc import Mapping\nfrom types import MappingProxyType\n"
            if any(isinstance(value, (dict, list)) for value in protocol.values())
            else ""
        )
        + "\n"
        + "".join(
            f"{key}: Final[Mapping[str, str]] = {protocol_literal(value)}\n"
            if isinstance(value, dict)
            and all(isinstance(item, str) for item in value.values())
            else f"{key}: Final = {protocol_literal(value)}\n"
            for key, value in sorted(protocol.items())
        )
    )
    formatted = format_code(protocol_content, CONTRACT / "protocol.py")
    outputs = [(CONTRACT / "protocol.py", formatted)]
    for name, class_name in (
        ("request", "CodegenRequest"),
        ("response", "CodegenResponse"),
        ("native", "NativeMcpBindingProfile"),
        ("diagnostic", "CodegenDiagnostic"),
    ):
        outputs.append((CONTRACT / f"{name}.py", project(name, class_name)))
    for target, content in outputs:
        if args.check:
            if not target.is_file() or target.read_text() != content:
                different.append(str(target.relative_to(ROOT)))
        else:
            target.write_text(content)
    if different:
        print("codegen contract drift: " + ", ".join(different), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
