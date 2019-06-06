from pytest import fixture, raises
from mediark.application.utilities import (
    TenantProvider, StandardTenantProvider, Tenant)


@fixture
def tenant_provider() -> TenantProvider:
    return StandardTenantProvider()


def test_tenant_provider_methods():
    abstract_methods = TenantProvider.__abstractmethods__

    assert 'setup' in abstract_methods


def test_standard_tenant_provider_instantiation(tenant_provider):
    assert isinstance(tenant_provider, TenantProvider)


def test_standard_tenant_provider_setup(tenant_provider):
    tenant = Tenant(name='Mode')
    assert tenant_provider.state.tenant is None
    tenant_provider.setup(tenant)
    assert tenant_provider.state.tenant == tenant


def test_standard_tenant_provider_get_tenant(tenant_provider):
    tenant = Tenant(name='Mode')
    assert tenant_provider.state.tenant is None
    tenant_provider.setup(tenant)
    assert tenant_provider.tenant == tenant


def test_standard_tenant_provider_get_tenant_not_set(tenant_provider):
    with raises(ValueError):
        assert tenant_provider.tenant
