from abc import ABC, abstractmethod
from typing import Dict, Any


class TenantSupplier(ABC):

    @abstractmethod
    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant method to be implemented."""

    @abstractmethod
    def create_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        """Create tenant method to be implemented."""

    @abstractmethod
    def resolve_tenant(self, name: str) -> Dict[str, Any]:
        """Resolve tenant method to be implemented."""
