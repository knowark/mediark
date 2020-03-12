from mediark.infrastructure.core import (
    SetupSupplier, MemorySetupSupplier)


def test_setup_supplier_methods() -> None:
    methods = SetupSupplier.__abstractmethods__  # type: ignore
    assert 'setup' in methods


def test_setup_supplier_setup() -> None:
    setup_supplier = MemorySetupSupplier()
    assert setup_supplier.setup() is None
