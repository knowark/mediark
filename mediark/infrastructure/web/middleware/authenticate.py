from typing import Callable, Optional, Any
from functools import wraps
from flask import request, jsonify
from ....application.coordinators import SessionCoordinator
from ...core import TenantSupplier, JwtSupplier, AuthenticationError
from ..schemas import UserSchema
import logging


class Authenticate:

    def __init__(self, jwt_supplier: JwtSupplier,
                 tenant_supplier: TenantSupplier,
                 session_coordinator: SessionCoordinator) -> None:
        self.jwt_supplier = jwt_supplier
        self.tenant_supplier = tenant_supplier
        self.session_coordinator = session_coordinator

    def __call__(self, method: Callable) -> Callable:
        @wraps(method)
        def decorator(*args, **kwargs):
            authorization = request.headers.get('Authorization', "")
            token = authorization.replace('Bearer ', '')
            if not token:
                aux = request.args.get('access_token')
                token = aux if aux is not None else ""

            try:
                token_payload = self.jwt_supplier.decode(
                    token, verify=False)

                tenant_dict = self.tenant_supplier.get_tenant(
                    token_payload['tid'])

                token_payload = self.jwt_supplier.decode(token, secret=None)

                self.session_coordinator.set_tenant(tenant_dict)

                user_dict = UserSchema().load(token_payload)

                self.session_coordinator.set_user(user_dict)

            except Exception as e:
                def error_function(*args, **kwargs):
                    return jsonify(error={
                        'exception': 'Unauthorized',
                        'message': str(AuthenticationError),
                        'trace': str(e)
                    }), 401
                logging.error(e)
                return error_function(*args, **kwargs)

            return method(*args, **kwargs)

        return decorator
