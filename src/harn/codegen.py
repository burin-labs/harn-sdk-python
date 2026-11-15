"""One-shot Python backend and thin entrypoint for Harn's generation host."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

from pydantic import ValidationError

from ._codegen.api import render
from ._codegen.diagnostic import CodegenDiagnostic, CodegenDiagnosticCode
from ._codegen.request import CodegenRequest, CodegenRole
from ._codegen.response import (
    CodegenFeature,
    CodegenIdentity,
    CodegenResponse,
    CodegenResponseVersion,
)
from ._codegen.types import GenerationError

SUPPORTED_FEATURES = (
    CodegenFeature.EXACT_JSON_INTEGER,
    CodegenFeature.BASE64_BYTES,
    CodegenFeature.CANONICAL_DECIMAL,
    CodegenFeature.SETS,
    CodegenFeature.TUPLES,
    CodegenFeature.STRING_MAPS,
    CodegenFeature.OPTIONAL_FIELDS,
    CodegenFeature.NOMINAL_TYPES,
    CodegenFeature.RECURSIVE_TYPES,
    CodegenFeature.DISJOINT_UNIONS,
    CodegenFeature.DECLARED_APPLICATION_ERRORS,
    CodegenFeature.MCP_TASKS,
    CodegenFeature.REQUEST_CANCELLATION,
)


def _diagnostic(code: CodegenDiagnosticCode, **fields: str | None) -> int:
    diagnostic = CodegenDiagnostic.model_validate(
        {"code": code, "structural_path": "request", **fields}
    )
    print(diagnostic.model_dump_json(), file=sys.stderr)
    return 2


def plugin() -> int:
    try:
        request = CodegenRequest.model_validate_json(sys.stdin.buffer.read())
    except ValidationError as error:
        failures = error.errors(
            include_input=False, include_context=False, include_url=False
        )
        if any(
            failure["type"] == "enum"
            and tuple(failure["loc"]) in (("schema_version",), ("ir", "schema_version"))
            for failure in failures
        ):
            return _diagnostic(CodegenDiagnosticCode.UNSUPPORTED_VERSION)
        if any(
            failure["type"] == "enum"
            and tuple(failure["loc"][:2]) == ("ir", "required_features")
            for failure in failures
        ):
            return _diagnostic(
                CodegenDiagnosticCode.UNSUPPORTED_FEATURE,
                structural_path="required_features",
            )
        return _diagnostic(CodegenDiagnosticCode.INVALID_IR)
    if any(
        feature.value not in {supported.value for supported in SUPPORTED_FEATURES}
        for feature in request.ir.required_features
    ):
        return _diagnostic(
            CodegenDiagnosticCode.UNSUPPORTED_FEATURE,
            structural_path="required_features",
        )
    for operation in request.ir.operations:
        if operation.output.kind == "missing":
            diagnostic = CodegenDiagnostic.model_validate(
                {
                    "code": CodegenDiagnosticCode.MISSING_OUTPUT,
                    "operation": operation.id,
                    "source": operation.source.model_dump(mode="json"),
                    "structural_path": "operations.output",
                }
            )
            print(diagnostic.model_dump_json(), file=sys.stderr)
            return 2
    try:
        artifact = render(request.ir, request.role)
    except GenerationError as error:
        diagnostic = CodegenDiagnostic.model_validate(
            {
                "code": CodegenDiagnosticCode.UNSUPPORTED_WIRE_TYPE,
                "structural_path": "types",
                "type_id": error.type_id,
                "source": error.source.model_dump(mode="json"),
                "operation": _owning_operation(request, error.type_id),
            }
        )
        print(diagnostic.model_dump_json(), file=sys.stderr)
        return 2
    except (KeyError, ValueError):
        return _diagnostic(CodegenDiagnosticCode.INVALID_IR)
    response = CodegenResponse(
        schema_version=CodegenResponseVersion.HARN_CODEGEN_RESPONSE_1_0,
        identity=CodegenIdentity.model_validate(
            request.ir.identity.model_dump(mode="json")
        ),
        supported_features=list(SUPPORTED_FEATURES),
        artifacts=[artifact],
    )
    print(response.model_dump_json())
    return 0


def _owning_operation(request: CodegenRequest, type_id: str) -> str | None:
    # This walks only closed IR edges. Catalog JSON and its schema are opaque.
    types = {wire.id: wire for wire in request.ir.types}
    for operation in sorted(request.ir.operations, key=lambda operation: operation.id):
        pending = [operation.input]
        if operation.output.kind == "value":
            pending.append(operation.output.type_id)
        if operation.application_error:
            pending.append(operation.application_error)
        seen = set()
        while pending:
            current = pending.pop()
            if current == type_id:
                return operation.id
            if current in seen:
                continue
            seen.add(current)
            shape = types[current].shape
            if shape.kind == "list" or shape.kind == "set":
                pending.append(shape.item)
            elif shape.kind == "tuple":
                pending.extend(shape.items)
            elif shape.kind == "map":
                pending.append(shape.value)
            elif shape.kind == "alias":
                pending.append(shape.target)
            elif shape.kind == "union":
                pending.extend(shape.members)
            elif shape.kind == "record":
                pending.extend(field.type_id for field in shape.fields)
                if shape.additional is not None:
                    pending.append(shape.additional)
            elif shape.kind == "enum":
                pending.extend(
                    field.type_id
                    for variant in shape.variants
                    for field in variant.fields
                )
    return None


def main() -> int:
    if len(sys.argv) == 1:
        return plugin()
    parser = argparse.ArgumentParser(
        description="Generate strict Python adapters with Harn's validated codegen host."
    )
    parser.add_argument("--file", required=True, type=Path, help="Harn source contract")
    parser.add_argument("--ir", type=Path, help="Optional frozen IR commitment")
    parser.add_argument("--surface", choices=("exports", "script"), default="exports")
    parser.add_argument("--select", action="append", default=[])
    parser.add_argument("--plugin-read-root", action="append", default=[], type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--role", choices=[role.value for role in CodegenRole], default="both"
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--harn", default="harn", help="Harn executable containing codegen generate"
    )
    args = parser.parse_args()
    executable = shutil.which(args.harn)
    backend = shutil.which("harn-codegen-python", path=sysconfig.get_path("scripts"))
    if executable is None or backend is None:
        return _diagnostic(CodegenDiagnosticCode.PLUGIN_SPAWN_FAILED)
    command = [
        executable,
        "codegen",
        "generate",
        "--file",
        str(args.file),
        "--surface",
        args.surface,
        "--plugin",
        str(backend),
        "--role",
        args.role,
        "--out",
        str(args.out),
    ]
    if args.ir is not None:
        command.extend(("--ir", str(args.ir)))
    for selection in args.select:
        command.extend(("--select", selection))
    roots = dict.fromkeys(
        Path(root).resolve()
        for root in (sys.prefix, sys.base_prefix, *args.plugin_read_root)
    )
    for root in roots:
        command.extend(("--plugin-read-root", str(root)))
    if args.check:
        command.append("--check")
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
