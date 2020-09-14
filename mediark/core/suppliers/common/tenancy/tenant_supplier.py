from abc import ABC, abstractmethod
from typing import List, Dict, Any


class TenantSupplier(ABC):
    @abstractmethod
    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant method to be implemented."""

    @abstractmethod
    def search_tenants(self, domain: List) -> List[Dict[str, Any]]:
        """Search tenants method to be implemented."""

    @abstractmethod
    def ensure_tenant(self, tenant_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure tenant method to be implemented."""
