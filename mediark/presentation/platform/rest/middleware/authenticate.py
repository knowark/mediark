import jwt
import json
from typing import Callable, Dict, Any
from aiohttp import web
from injectark import Injectark
from .....application.operation.managers import SessionManager


def authenticate_middleware_factory(injector: Injectark) -> Callable:
    session_manager: SessionManager = injector['SessionManager']
    secret = injector.config.get('secrets', {}).get('tokens', '')

    @web.middleware
    async def middleware(request: web.Request, handler: Callable):
        ignored = ('/favicon',)
        if request.path.startswith(ignored):
            return web.Response()

        public = ('/download',)
        if request.path == '/' or request.path.startswith(public):
            return await handler(request)

        token = request.headers.get(
            'Authorization', '').replace('Bearer ', '')
        token = token or request.query.get('access_token', '')

        try:

            payload  = jwt.decode(token, secret, algorithms=['HS256'],
                                  options={"verify_signature": bool(secret)})

            user_dict = extract_user(payload)
            await session_manager.set_user(user_dict)

            tenant = payload['tenant']
            tenant_id = payload['tid']

            tenant_dict = await session_manager.ensure_tenant(
                {'id': tenant_id, 'name': tenant})
            await session_manager.set_tenant(tenant_dict)
        except Exception as error:
            reason = f"{error.__class__.__name__}: {str(error)}"
            raise web.HTTPUnauthorized(reason=reason)

        return await handler(request)

    return middleware


def extract_user(headers: Dict[str, Any]) -> Dict[str, Any]:
    user_id = headers['uid']
    email = headers.get('email', "@")
    name = headers.get('name', '')
    roles = headers.get('roles', '')

    return {
        'id': user_id,
        'name': name,
        'email': email,
        'roles': roles
    }
