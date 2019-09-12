from mediark.infrastructure.core import TenantSupplier, MemoryTenantSupplier


def test_tenant_supplier_methods() -> None:
    methods = TenantSupplier.__abstractmethods__  # type: ignore
    assert 'get_tenant' in methods
    assert 'create_tenant' in methods


def test_memory_tenant_supplier_create_get_search_tenant() -> None:
    tenant_supplier = MemoryTenantSupplier()

    assert tenant_supplier.get_tenant('1')['name'] == 'origin'

    assert len(tenant_supplier.search_tenants([["name", "=", "origin"]])) == 1
