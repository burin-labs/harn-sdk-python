from harn import ProtocolClient, create_harn_protocol_client
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

print("Verified installed typed protocol package.")
