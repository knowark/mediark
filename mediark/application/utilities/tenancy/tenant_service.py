from abc import ABC, abstractmethod
from threading import local
from .tenant import Tenant


class TenantService(ABC):
    """Tenant service."""

    @abstractmethod
    def setup(self, tenant: Tenant) -> None:
        "Setup current tenant method to be implemented."

    @property
    @abstractmethod
    def tenant(self) -> Tenant:
        """Get the current tenant"""


class StandardTenantService(TenantService):

    def __init__(self, tenant=None) -> None:
        self.state = local()
        self.state.__dict__.setdefault('tenant', tenant)

    def setup(self, tenant: Tenant) -> None:
        self.state.tenant = tenant

    @property
    def tenant(self) -> Tenant:
        if not self.state.tenant:
            raise ValueError('No tenant has been set.')
        return self.state.tenant
