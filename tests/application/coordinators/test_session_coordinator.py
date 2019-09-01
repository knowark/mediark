import jwt
from typing import Dict, cast
from pytest import fixture
from mediark.application.utilities import (
    TenantProvider, StandardTenantProvider, Tenant)
from mediark.application.services import (
    AuthService, StandardAuthService)
from mediark.application.coordinators import SessionCoordinator


@fixture
def auth_service() -> AuthService:
    return StandardAuthService('maindominion')


@fixture
def tenant_provider() -> TenantProvider:
    return StandardTenantProvider()


@fixture
def session_coordinator(
        tenant_provider: TenantProvider,
        auth_service: StandardAuthService) -> SessionCoordinator:
    return SessionCoordinator(tenant_provider, auth_service)


def test_session_coordinator_creation(
        session_coordinator: SessionCoordinator) -> None:
    assert hasattr(session_coordinator, 'set_tenant')
    assert hasattr(session_coordinator, 'get_tenant')
    assert hasattr(session_coordinator, 'set_user')


def test_session_coordinator_set_tenant(
        session_coordinator: SessionCoordinator) -> None:

    tenant = {'name': 'Default'}
    session_coordinator.set_tenant(tenant)
    assert session_coordinator


def test_session_coordinator_get_tenant(
        session_coordinator: SessionCoordinator) -> None:

    session_coordinator.set_tenant({'name': 'Default'})
    tenant = session_coordinator.get_tenant()
    assert isinstance(tenant, dict)
    assert tenant['name'] == 'Default'


def test_session_coordinator_set_user(
        session_coordinator: SessionCoordinator) -> None:

    user = {'name': 'jdacevedo'}
    session_coordinator.set_user(user)
    assert session_coordinator.auth_service.user.name == 'jdacevedo'
