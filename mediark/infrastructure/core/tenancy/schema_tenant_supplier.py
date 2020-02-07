from typing import Dict, Any
from tenark.models import Tenant
from tenark.resolver import resolve_managers
from .memory_tenant_supplier import MemoryTenantSupplier


class SchemaTenantSupplier(MemoryTenantSupplier):

    def __init__(self, catalog_dsn: str, zones: Dict[str, str]) -> None:
        self.arranger, self.provider = resolve_managers({
            'cataloguer_kind': 'schema',
            'catalog_dsn': catalog_dsn,
            'provisioner_kind': 'schema',
            'provision_schema_zones': zones
        })
