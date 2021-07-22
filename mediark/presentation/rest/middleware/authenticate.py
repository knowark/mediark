import json
from typing import Callable, Dict, Any
from aiohttp import web
from injectark import Injectark
from ....application.managers import SessionManager
from ....integration.core.suppliers.common.tenancy import TenantSupplier


def authenticate_middleware_factory(injector: Injectark) -> Callable:
    session_manager: SessionManager = injector['SessionManager']
    tenant_supplier: TenantSupplier = injector['TenantSupplier']

    @web.middleware
    async def middleware(request: web.Request, handler: Callable):
        public = ('/favicon', '/download')
        if request.path == '/' or request.path.startswith(public):
            return await handler(request)

        try:
            user_dict = extract_user(request.headers)
            session_manager.set_user(user_dict)

            tenant = request.headers['Tenant']
            tenant_id = request.headers['TenantId']

            tenant_dict = tenant_supplier.ensure_tenant(
                {'id': tenant_id, 'name': tenant})
            session_manager.set_tenant(tenant_dict)
        except Exception as error:
            reason = f"{error.__class__.__name__}: {str(error)}"
            raise web.HTTPUnauthorized(reason=reason)

        return await handler(request)

    return middleware


def extract_user(headers: Dict[str, Any]) -> Dict[str, Any]:
    user_id = headers['UserId']
    email = headers.get('From', "@")
    name = email.split('@')[0]
    roles = headers.get('Roles', '').strip().split(',')

    return {
        'id': user_id,
        'name': name,
        'email': email,
        'roles': roles
    }
