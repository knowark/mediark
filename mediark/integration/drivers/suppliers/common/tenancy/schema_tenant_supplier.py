from typing import Dict, Any
from tenark.models import Tenant
from tenark.resolver import resolve_managers
from ......application.general.suppliers import MemoryTenantSupplier
from ..connection import SchemaConnection


class SchemaTenantSupplier(MemoryTenantSupplier):
    def __init__(self, connection: SchemaConnection,
                 zones: Dict[str, str]) -> None:
        self.arranger, self.provider = resolve_managers({
            'cataloguer_kind': 'schema',
            'catalog_connection': connection,
            'provisioner_kind': 'schema',
            'provision_schema_zones': zones
        })
        self.arranger.cataloguer.placeholder = '%s'
