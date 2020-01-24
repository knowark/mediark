from pytest import fixture, raises
from mediark.application.utilities.tenancy import (
    TenantProvider, StandardTenantProvider, Tenant)


def test_tenant_provider_methods():
    abstract_methods = str(getattr(TenantProvider, "__abstractmethods__"))
    assert 'setup' in abstract_methods


def test_standard_tenant_provider_instantiation(tenant_provider):
    assert isinstance(tenant_provider, TenantProvider)


def test_standard_tenant_provider_setup(tenant_provider):
    tenant = Tenant(name='Alpina')
    tenant_provider.setup(None)
    tenant_provider.setup(tenant)
    assert tenant_provider.tenant == tenant


def test_standard_tenant_provider_get_tenant_not_set(tenant_provider):
    tenant_provider.setup(None)
    with raises(ValueError):
        assert tenant_provider.tenant
