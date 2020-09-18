from pytest import fixture
from mediark.core.suppliers import SchemaMigrationSupplier
from mediark.core.suppliers.common.tenancy import MemoryTenantSupplier
from mediark.core.suppliers.migration import (
    schema_migration_supplier as schema_migration_supplier_module)


@fixture
def mock_tenant_supplier():
    tenant_supplier = MemoryTenantSupplier()
    tenant_supplier.ensure_tenant({
        'id': '001',
        'name': 'Origin'
    })
    tenant_supplier.ensure_tenant({
        'id': '002',
        'name': 'External',
        'zone': 'MISTERY_ZONE'
    })
    return tenant_supplier


@fixture
def schema_migration_supplier(mock_tenant_supplier):
    zones = {
        "default": "postgresql://mediark:mediark@localhost/mediark"
    }
    return SchemaMigrationSupplier(zones, mock_tenant_supplier)


def test_schema_migration_supplier_instantiation(
        schema_migration_supplier) -> None:
    assert schema_migration_supplier is not None


def test_schema_migration_supplier_migrate(
        schema_migration_supplier, monkeypatch) -> None:

    arguments = {}

    def mock_sql_migrate(connection, path, schema, context, target_version):
        nonlocal arguments
        arguments['schema'] = schema
        arguments['target_version'] = target_version

    monkeypatch.setattr(
        schema_migration_supplier_module, 'sql_migrate', mock_sql_migrate)

    provider = schema_migration_supplier.tenant_supplier.provider
    catalog = provider.cataloguer.catalog
    assert '001' in catalog

    schema_migration_supplier.migrate()

    assert arguments == {
        'schema': 'origin',
        'target_version': '999'
    }


def test_schema_migration_supplier_migrate_missing(
        schema_migration_supplier) -> None:

    schema_migration_supplier.migrate('missing')
