from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path

import yaml

PROTOCOL_ROOT = Path("src/harn/protocol")
EXPECTED_MANIFEST = """language=python
harn_version=0.10.116
sdk_version=0.10.0
openapi_spec=spec/openapi.yaml
openapi_sha256=279739bbe7aff1242dcdb68d6061776277927701b8e0da3fd1d80120b200557a
generator=openapi-python-client@0.28.3
"""
EXPECTED_SPEC_SHA256 = (
    "279739bbe7aff1242dcdb68d6061776277927701b8e0da3fd1d80120b200557a"
)
EXPECTED_NORMALIZED_ARTIFACT_SHA256 = (
    "666a6483a19668a2562723176ed7f4c83b5a3e18160ba3edac2e8f34a5eac03f"
)


def main() -> None:
    manifest = (PROTOCOL_ROOT / "harn-sdk-generation.txt").read_text()
    assert_equal(manifest, EXPECTED_MANIFEST, "generation manifest")

    spec_source = Path("spec/openapi.yaml").read_bytes()
    assert_equal(
        hashlib.sha256(spec_source).hexdigest(),
        EXPECTED_SPEC_SHA256,
        "OpenAPI SHA-256",
    )
    assert_equal(
        hash_tree(PROTOCOL_ROOT),
        EXPECTED_NORMALIZED_ARTIFACT_SHA256,
        "artifact SHA-256",
    )

    document = yaml.safe_load(spec_source)
    operation_ids = {
        operation["operationId"]
        for path_item in document["paths"].values()
        for operation in path_item.values()
        if isinstance(operation, dict) and "operationId" in operation
    }
    modules = {
        path.stem
        for path in (PROTOCOL_ROOT / "api").rglob("*.py")
        if path.name != "__init__.py"
    }
    expected_modules = {to_snake_case(name) for name in operation_ids}
    assert_equal(len(operation_ids), 85, "OpenAPI operation count")
    assert_equal(modules, expected_modules, "generated operation modules")
    check_typed_entry_points(modules)
    print("Verified Harn v0.10.116 Python protocol artifact: 85 operations.")


def hash_tree(root: Path) -> str:
    digest = hashlib.sha256()
    paths = (
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".py", ".txt"}
    )
    for path in sorted(paths):
        if path.suffix == ".py":
            ast.parse(path.read_text())
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def check_typed_entry_points(modules: set[str]) -> None:
    for module in modules:
        matches = list((PROTOCOL_ROOT / "api").rglob(f"{module}.py"))
        tree = ast.parse(matches[0].read_text())
        functions = {
            node.name: node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        for name in ("sync", "asyncio"):
            function = functions.get(name)
            if function is None or function.returns is None:
                raise AssertionError(f"{module}.{name} is not a typed entry point")


def to_snake_case(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(
            f"{label} does not match the pinned Harn v0.10.116 artifact"
        )


if __name__ == "__main__":
    main()
