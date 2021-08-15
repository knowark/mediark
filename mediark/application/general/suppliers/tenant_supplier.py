from abc import ABC, abstractmethod
from typing import List, Dict, Any
from tenark.models import Tenant
from tenark.resolver import resolve_managers


class TenantSupplier(ABC):
    @abstractmethod
    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant method to be implemented."""

    @abstractmethod
    def search_tenants(self, domain: List) -> List[Dict[str, Any]]:
        """Search tenants method to be implemented."""

    @abstractmethod
    def resolve_tenant(self, name: str) -> Dict[str, Any]:
        """Resolve tenant method to be implemented."""

    @abstractmethod
    def ensure_tenant(self, tenant_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure tenant method to be implemented."""


class MemoryTenantSupplier(TenantSupplier):
    def __init__(self) -> None:
        self.arranger, self.provider = resolve_managers({})

    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        return self.provider.get_tenant(tenant_id)

    def search_tenants(self, domain: List) -> List[Dict[str, Any]]:
        return self.provider.search_tenants(domain)

    def resolve_tenant(self, name: str) -> Dict[str, Any]:
        return self.provider.resolve_tenant(name)

    def ensure_tenant(self, tenant_dict: Dict[str, Any]) -> Dict[str, Any]:
        return self.arranger.ensure_tenant(tenant_dict)
