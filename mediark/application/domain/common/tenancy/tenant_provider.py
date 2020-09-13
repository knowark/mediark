from abc import ABC, abstractmethod
from typing import Optional
from contextvars import ContextVar
from .tenant import Tenant


class TenantProvider(ABC):
    """Tenant service."""

    @abstractmethod
    def setup(self, tenant: Tenant) -> None:
        "Setup current tenant method to be implemented."

    @property
    @abstractmethod
    def tenant(self) -> Tenant:
        """Get the current tenant"""

    @property
    def location(self) -> str:
        return self.tenant.slug

    @property
    def zone(self) -> str:
        return self.tenant.zone


tenant_var: ContextVar[Optional[Tenant]] = ContextVar('tenant', default=None)


class StandardTenantProvider(TenantProvider):

    def setup(self, tenant: Tenant) -> None:
        tenant_var.set(tenant)

    @property
    def tenant(self) -> Tenant:
        tenant = tenant_var.get()
        if not tenant:
            raise ValueError('No tenant has been set.')
        return tenant
