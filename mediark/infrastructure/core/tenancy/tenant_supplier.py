from abc import ABC, abstractmethod
from typing import Dict, Any
from tenark.resolver import (
    resolve_cataloguer, resolve_provider, resolve_arranger)


class TenantSupplier(ABC):

    @abstractmethod
    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant method to be implemented."""

    @abstractmethod
    def create_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        """Create tenant method to be implemented."""

    @abstractmethod
    def search_tenants(self, domain):
        """Search tenant method to be implemented."""


class MemoryTenantSupplier(TenantSupplier):

    def __init__(self) -> None:
        cataloguer = resolve_cataloguer({})
        self.provider = resolve_provider({
            'cataloguer': cataloguer
        })
        self.arranger = resolve_arranger({
            'cataloguer': cataloguer
        })

    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        return self.provider.get_tenant(tenant_id)

    def create_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        self.arranger.create_tenant(tenant_dict)

    def search_tenants(self, domain):
        return self.provider.search_tenants(domain)
