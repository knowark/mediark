import rapidjson as json
from typing import Callable, Dict, Any
from aiohttp import web
from injectark import Injectark
from ....application.coordinators import SessionCoordinator
from ...core import TenantSupplier


def authenticate_middleware_factory(injector: Injectark) -> Callable:
    session_coordinator: SessionCoordinator = injector['SessionCoordinator']
    tenant_supplier: TenantSupplier = injector['TenantSupplier']

    @web.middleware
    async def middleware(request: web.Request, handler: Callable):
        if request.path == '/':
            return await handler(request)

        try:
            user_dict = extract_user(request.headers)
            session_coordinator.set_user(user_dict)

            tenant_id = request.headers['TenantId']
            tenant_dict = tenant_supplier.get_tenant(tenant_id)
            session_coordinator.set_tenant(tenant_dict)
        except Exception as e:
            raise web.HTTPUnauthorized(
                body=json.dumps({
                    "errors": [
                        {"message": f"{e.__class__.__name__}: {str(e)}"}
                    ]
                }))

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
