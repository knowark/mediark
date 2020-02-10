from shiftark.infrastructure.core import (
    TenantSupplier, MemoryTenantSupplier)


def test_tenant_supplier_methods() -> None:
    methods = TenantSupplier.__abstractmethods__  # type: ignore
    assert 'get_tenant' in methods
    assert 'create_tenant' in methods


def test_memory_tenant_supplier_create_and_get_tenant() -> None:
    tenant_supplier = MemoryTenantSupplier()
    tenant_supplier.create_tenant({
        'id': '001',
        'name': 'Knowark'
    })

    assert tenant_supplier.get_tenant('001')['name'] == 'Knowark'


def test_memory_tenant_supplier_create_and_resolve_tenant() -> None:
    tenant_supplier = MemoryTenantSupplier()
    tenant_supplier.create_tenant({
        'id': '001',
        'name': 'Knowark'
    })

    assert tenant_supplier.resolve_tenant('knowark')['name'] == 'Knowark'
