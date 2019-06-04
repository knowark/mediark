from pytest import fixture, raises
from mediark.application.utilities import (
    TenantService, StandardTenantService, Tenant)


@fixture
def tenant_service() -> TenantService:
    return StandardTenantService()


def test_tenant_service_methods():
    abstract_methods = TenantService.__abstractmethods__

    assert 'setup' in abstract_methods


def test_standard_tenant_service_instantiation(tenant_service):
    assert isinstance(tenant_service, TenantService)


def test_standard_tenant_service_setup(tenant_service):
    tenant = Tenant(name='Mode')
    assert tenant_service.state.tenant is None
    tenant_service.setup(tenant)
    assert tenant_service.state.tenant == tenant


def test_standard_tenant_service_get_tenant(tenant_service):
    tenant = Tenant(name='Mode')
    assert tenant_service.state.tenant is None
    tenant_service.setup(tenant)
    assert tenant_service.tenant == tenant


def test_standard_tenant_service_get_tenant_not_set(tenant_service):
    with raises(ValueError):
        assert tenant_service.tenant
