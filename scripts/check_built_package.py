import importlib.resources
import json
import shutil
import subprocess

from pydantic import StrictInt, TypeAdapter

from harn import ProtocolClient, create_harn_protocol_client
from harn._codegen.diagnostic import CodegenDiagnostic
from harn._codegen.request import CodegenRequest
from harn._mcp_server import NativeServer
from harn.bindings import BindingError, WireSet, parse_wire_json
from harn.protocol.api.permissions import check_permission
from harn.protocol.api.runtime import get_provider_catalog
from harn.protocol.models import PermissionCheckRequest, ProviderCatalog

assert ProtocolClient is not None
assert callable(create_harn_protocol_client)
assert callable(check_permission.sync)
assert callable(check_permission.asyncio)
assert callable(get_provider_catalog.sync)
assert ProviderCatalog is not None
assert PermissionCheckRequest is not None
assert (
    NativeServer is not None
    and CodegenRequest is not None
    and CodegenDiagnostic is not None
)
assert WireSet([True, 1]) != WireSet([True])
assert parse_wire_json(TypeAdapter(StrictInt), "1") == 1
try:
    parse_wire_json(TypeAdapter(StrictInt), "-0")
except BindingError:
    pass
else:
    raise AssertionError(
        "Installed wheel accepted a floating negative zero as an integer"
    )
schema_root = importlib.resources.files("harn._codegen").joinpath("schemas")
for name in ("ir", "request", "response", "native", "diagnostic"):
    schema = json.loads(schema_root.joinpath(f"{name}-v1.json").read_text())
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False and schema["properties"]
command = shutil.which("harn-codegen-python")
assert command is not None
subprocess.run([command, "--help"], check=True, capture_output=True)

print("Verified installed typed protocol package.")
