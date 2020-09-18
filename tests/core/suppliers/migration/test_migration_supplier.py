from mediark.core.suppliers import (
    MigrationSupplier, MemoryMigrationSupplier)


def test_migration_supplier_methods() -> None:
    methods = MigrationSupplier.__abstractmethods__  # type: ignore
    assert 'migrate' in methods


def test_memory_migration_supplier_migrate() -> None:
    migration_supplier = MemoryMigrationSupplier()

    assert migration_supplier.migrate() is None
