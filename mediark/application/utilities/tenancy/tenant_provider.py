from abc import ABC, abstractmethod
from aiocontextvars import ContextVar
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


tenant_var = ContextVar('tenant', default=None)


class StandardTenantProvider(TenantProvider):

    def setup(self, tenant: Tenant) -> None:
        tenant_var.set(tenant)

    @property
    def tenant(self) -> Tenant:
        if not tenant_var.get():
            raise ValueError('No tenant has been set.')
        return tenant_var.get()
