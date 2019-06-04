from typing import Dict, Any
from ..utilities import TenantProvider, Tenant
from ..services import AuthService, User


class SessionCoordinator:
    def __init__(self, tenant_provider: TenantProvider,
                 auth_service: AuthService) -> None:
        self.tenant_provider = tenant_provider
        self.auth_service = auth_service

    def set_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        tenant = Tenant(**tenant_dict)
        self.tenant_provider.setup(tenant)

    def get_tenant(self) -> Dict[str, Any]:
        tenant = self.tenant_provider.tenant
        return vars(tenant)
    
    def set_user(self, user_dict: Dict[str, Any]) -> None:
        user = User(**user_dict)
        self.auth_service.setup(user)
