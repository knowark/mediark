import time
import datetime
from typing import Dict, Union, Any
from ...domain.common import TenantProvider, Tenant, AuthProvider, User
from ...domain.common.auth import anonymous_user, system_user
from ...domain.common.tenancy import anonymous_tenant, system_tenant
from ...general.suppliers import TenantSupplier


class SessionManager:
    def __init__(self, tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 tenant_supplier: TenantSupplier) -> None:
        self.tenant_provider = tenant_provider
        self.auth_provider = auth_provider
        self.tenant_supplier = tenant_supplier

    async def set_anonymous(self, entry: dict) -> dict:
        self.tenant_provider.setup(anonymous_tenant)
        self.auth_provider.setup(anonymous_user)
        return {}

    async def set_system(self, entry: dict) -> dict:
        self.tenant_provider.setup(system_tenant)
        self.auth_provider.setup(system_user)
        return {}

    async def set_tenant(self, entry: dict) -> dict:
        tenant = Tenant(**entry)
        self.tenant_provider.setup(tenant)
        return {}

    async def get_tenant(self, entry: dict) -> dict:
        current = self.tenant_provider.tenant
        return vars(current)

    async def set_user(self, entry: dict) -> dict:
        user = User(**entry)
        self.auth_provider.setup(user)
        return {}

    async def resolve_tenant(self, entry: dict) -> dict:
        return self.tenant_supplier.resolve_tenant(entry['data'])

    async def ensure_tenant(self, entry: dict) -> dict:
        return self.tenant_supplier.ensure_tenant(entry)
