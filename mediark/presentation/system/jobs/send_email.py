import jwt
from typing import Dict, Any
from injectark import Injectark, Config
from schedulark import Task


class SendEmailJob:
    def __init__(self, injector: Injectark) -> None:
        self.config = injector.config
        self.injector = injector
        self.email_manager = injector['EmailManager']

    async def __call__(self, task: Task) -> dict:
        session_manager = self.injector['SessionManager']
        payload = task.payload
        authorization = payload['meta']['authorization']
        secret = self.config.get('secrets', {}).get('tokens') or ""

        try:

            auth_dict  = jwt.decode(authorization, secret, algorithms=['HS256'],
                                  options={"verify_signature": bool(secret)})

            user_dict = extract_user(auth_dict)
            await session_manager.set_user(user_dict)

            tenant = auth_dict['tenant']
            tenant_id = auth_dict['tid']

            tenant_dict = await session_manager.ensure_tenant(
                {'id': tenant_id, 'name': tenant})
            await session_manager.set_tenant(tenant_dict)
        except Exception as error:
            reason = f"{error.__class__.__name__}: {str(error)}"

            return {"error": reason}

        entry: dict = {
            "data": payload['data'],
            "meta": {}
        }
        await self.email_manager.send(entry)

        return {}

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
