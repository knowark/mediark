from typing import List, Dict, Any
from tenark.models import Tenant
from tenark.resolver import resolve_managers
from .tenant_supplier import TenantSupplier


class MemoryTenantSupplier(TenantSupplier):
    def __init__(self) -> None:
        self.arranger, self.provider = resolve_managers({})

    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        return self.provider.get_tenant(tenant_id)

    def search_tenants(self, domain: List) -> List[Dict[str, Any]]:
        return self.provider.search_tenants(domain)

    def ensure_tenant(self, tenant_dict: Dict[str, Any]) -> Dict[str, Any]:
        return self.arranger.ensure_tenant(tenant_dict)
