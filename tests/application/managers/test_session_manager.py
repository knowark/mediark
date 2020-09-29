from pytest import fixture
from mediark.application.domain.common import (
    TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from mediark.application.managers import SessionManager


@fixture
def session_manager(tenant_provider, auth_provider):
    return SessionManager(tenant_provider, auth_provider)


@fixture
def auth_provider() -> AuthProvider:
    return StandardAuthProvider()


@fixture
def tenant_provider() -> TenantProvider:
    return StandardTenantProvider()


@fixture
def session_manager(
        tenant_provider: TenantProvider,
        auth_provider: AuthProvider) -> SessionManager:
    return SessionManager(tenant_provider, auth_provider)


def test_session_manager_creation(
        session_manager: SessionManager) -> None:
    assert hasattr(session_manager, 'set_tenant')
    assert hasattr(session_manager, 'get_tenant')
    assert hasattr(session_manager, 'set_user')


def test_session_manager_set_tenant(
        session_manager: SessionManager) -> None:

    tenant = {'name': 'Default'}
    session_manager.set_tenant(tenant)
    assert session_manager


def test_session_manager_get_tenant(
        session_manager: SessionManager) -> None:

    session_manager.set_tenant({'name': 'Default'})
    tenant = session_manager.get_tenant()
    assert isinstance(tenant, dict)
    assert tenant['name'] == 'Default'


def test_session_manager_set_user(
        session_manager: SessionManager) -> None:

    user = {'name': 'jdacevedo'}
    session_manager.set_user(user)
    assert session_manager.auth_provider.user.name == 'jdacevedo'
