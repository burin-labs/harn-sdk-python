"""The same Harn-owned graph drives strict static and runtime boundaries."""

import asyncio
import copy
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import TypeAdapter

from harn._codegen.api import render
from harn._codegen.request import CodegenIr, CodegenRole
from harn._mcp_server import NativeServer
from harn._wire_json import loads
from harn.bindings import BindingError

FIXTURE = Path(__file__).parent / "fixtures/codegen/pathological"


def rich_ir():
    return CodegenIr.model_validate_json((FIXTURE / "ir.json").read_bytes())


def generated(tmp_path, role=CodegenRole.BOTH):
    artifact = render(rich_ir(), role)
    path = tmp_path / artifact.path
    path.write_text(artifact.content)
    spec = importlib.util.spec_from_file_location("generated_bindings", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_all_roles_and_reordered_nodes_are_deterministic(tmp_path):
    ir = rich_ir()
    assert len(ir.types) == 32 and len(ir.operations) == 4
    for role in CodegenRole:
        artifact = render(ir, role)
        reordered = ir.model_copy(
            update={
                "types": list(reversed(ir.types)),
                "operations": list(reversed(ir.operations)),
            }
        )
        assert artifact == render(reordered, role)
        module = generated(tmp_path, role)
        assert hasattr(module, "Client") == (role != CodegenRole.SERVER)
        assert hasattr(module, "create_server") == (role != CodegenRole.CLIENT)
        assert (module.CATALOG_DIGEST, module.BINDING_DIGEST, module.IR_DIGEST) == (
            ir.identity.catalog_digest,
            ir.identity.binding_digest,
            ir.identity.ir_digest,
        )
        encoded = artifact.content.encode()
        assert len(artifact.source_mappings) >= len(ir.types)
        assert all(
            encoded[mapping.start : mapping.end] for mapping in artifact.source_mappings
        )


def test_native_registry_is_exact_and_instance_owned(tmp_path):
    module = generated(tmp_path)

    def echo(arguments):
        return arguments.input

    async def async_echo(arguments):
        return arguments.input

    handlers = dict.fromkeys(["echo", "mutate", "reject", "scheduled"], echo)
    first = module.create_server(handlers)
    second = module.create_server(handlers)
    assert first is not second
    original = list(first._bindings.values())
    for bindings in ([*original, original[0]], [original[0]]):
        with pytest.raises(
            BindingError, match="duplicate_native_registration|native_tool_census"
        ):
            NativeServer(
                bindings,
                rich_ir().mcp_tools,
                rich_ir().identity.model_dump(mode="json"),
            )
    for malformed in ({}, {**handlers, "extra": echo}, {**handlers, "echo": None}):
        with pytest.raises(BindingError, match="native_handler_census"):
            module.create_server(malformed)
    with pytest.raises(BindingError, match="expected_sync_handler"):
        module.create_server({**handlers, "echo": async_echo})
    with pytest.raises(BindingError, match="expected_async_handler"):
        module.create_async_server(handlers)


def test_rich_native_handler_rejects_bad_input_and_bad_output(tmp_path):
    module = generated(tmp_path)
    raw = (FIXTURE / "input.json").read_text()
    payload = TypeAdapter(module.EchoInput).validate_json('{"input":' + raw + "}")

    def echo(arguments):
        return arguments.input

    server = module.create_server(
        dict.fromkeys(["echo", "mutate", "reject", "scheduled"], echo)
    )
    binding = server._bindings["echo"]
    assert binding.invoke(loads('{"input":' + raw + "}"))["structuredContent"] == loads(
        raw
    )
    assert payload.input.amount.as_tuple().exponent == -4
    with pytest.raises(BindingError, match="invalid_wire_value"):
        binding.invoke({"input": {}})

    def invalid(_arguments):
        # An unsafe user can construct a model without validation; admission must still refuse.
        return module.Payload.model_construct(tag="payload", sequence=True)

    malformed = module.create_server(
        dict.fromkeys(["echo", "mutate", "reject", "scheduled"], invalid)
    )
    with pytest.raises(BindingError, match="invalid_native_value"):
        malformed._bindings["echo"].invoke(loads('{"input":' + raw + "}"))


def test_no_schema_free_global_registry_remains():
    import harn

    assert not hasattr(harn, "registry") and not hasattr(harn, "tool")
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("harn.tools")


def test_official_mcp_result_forwards_opaque_tool_extensions_and_nulls(tmp_path):
    module = generated(tmp_path)

    def echo(arguments):
        return arguments.input

    measured = module.create_server(
        dict.fromkeys(["echo", "mutate", "reject", "scheduled"], echo)
    )
    tools = copy.deepcopy(rich_ir().mcp_tools)
    tools[0]["futureExtension"] = {"opaque": None}
    tools[0]["description"] = None
    server = NativeServer(
        list(measured._bindings.values()),
        tools,
        rich_ir().identity.model_dump(mode="json"),
    )

    async def next_result(_ctx):
        result = await server._list(None, None)
        return result.model_dump(mode="json", by_alias=True, exclude_none=True)

    ctx = SimpleNamespace(request_id="measured", method="tools/list")
    assert asyncio.run(server._project_tools(ctx, next_result))["tools"] == tools
