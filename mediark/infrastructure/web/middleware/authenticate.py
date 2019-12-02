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
            tenant_id = request.headers['TenantId']
            user_id = request.headers.get('UserId')
            email = request.headers.get('From', "@")
            name = email.split('@')[0]
            roles = request.headers.get('Roles', '').strip().split(',')

            user_dict = {
                'id': user_id,
                'name': name,
                'email': email,
                'roles': roles
            }
            self.session_coordinator.set_user(user_dict)

            tenant_dict = self.tenant_supplier.get_tenant(tenant_id)
            self.session_coordinator.set_tenant(tenant_dict)

            return method(*args, **kwargs)

        return decorator
