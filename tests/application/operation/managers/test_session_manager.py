import jwt
from typing import Dict, cast
from pytest import fixture
from mediark.application.domain.common import (
    TenantProvider, StandardTenantProvider, Tenant,
    AuthProvider, StandardAuthProvider, User)
from mediark.application.general.suppliers import (
    TenantSupplier, MemoryTenantSupplier)
from mediark.application.operation.managers import (
    SessionManager)


@fixture
def auth_provider() -> AuthProvider:
    return StandardAuthProvider()


@fixture
def tenant_provider() -> TenantProvider:
    return StandardTenantProvider()


@fixture
def tenant_supplier() -> TenantSupplier:
    return MemoryTenantSupplier()


@fixture
def session_manager(
    tenant_provider: TenantProvider,
    auth_provider: AuthProvider,
    tenant_supplier: TenantSupplier
) -> SessionManager:
    return SessionManager(tenant_provider, auth_provider, tenant_supplier)


def test_session_manager_creation(
        session_manager: SessionManager) -> None:
    assert hasattr(session_manager, 'set_tenant')
    assert hasattr(session_manager, 'get_tenant')
    assert hasattr(session_manager, 'set_user')


async def test_session_manager_set_tenant(
        session_manager: SessionManager) -> None:

    tenant = {'name': 'Default'}
    await session_manager.set_tenant(tenant)
    assert session_manager


async def test_session_manager_get_tenant(
        session_manager: SessionManager) -> None:

    await session_manager.set_tenant({'name': 'Default'})
    tenant = await session_manager.get_tenant({})
    assert isinstance(tenant, dict)
    assert tenant['name'] == 'Default'


async def test_session_manager_set_user(
        session_manager: SessionManager) -> None:

    user = {'name': 'jdacevedo'}
    await session_manager.set_user(user)
    assert session_manager.auth_provider.user.name == 'jdacevedo'


async def test_session_manager_set_system(
        session_manager: SessionManager) -> None:

    await session_manager.set_system({})
    assert session_manager.auth_provider.user.name == 'system'


async def test_session_manager_set_anonymous(
        session_manager: SessionManager) -> None:

    await session_manager.set_anonymous({})
    assert session_manager.auth_provider.user.name == 'anonymous'


async def test_session_manager_ensure_tenant(session_manager) -> None:
    await session_manager.ensure_tenant({'id': 'T001', 'name': 'Knowark'})

    tenants = session_manager.tenant_supplier.search_tenants([])

    assert len(tenants) == 1
    assert tenants[0]['id'] == 'T001'
    assert tenants[0]['slug'] == 'knowark'
