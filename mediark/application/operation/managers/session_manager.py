from typing import Dict, Any
from ...domain.common import TenantProvider, Tenant, AuthProvider, User


class SessionManager:
    def __init__(self, tenant_provider: TenantProvider,
                 auth_provider: AuthProvider) -> None:
        self.tenant_provider = tenant_provider
        self.auth_provider = auth_provider

    def set_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        tenant = Tenant(**tenant_dict)
        self.tenant_provider.setup(tenant)

    def get_tenant(self) -> Dict[str, Any]:
        current = self.tenant_provider.tenant
        return vars(current)

    def set_user(self, user_dict: Dict[str, Any]) -> None:
        user = User(**user_dict)
        self.auth_provider.setup(user)
