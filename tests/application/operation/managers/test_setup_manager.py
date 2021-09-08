import jwt
from typing import Dict, cast
from pytest import fixture
from mediark.application.domain.common import (
    TenantProvider, StandardTenantProvider, Tenant,
    AuthProvider, StandardAuthProvider, User)
from mediark.application.general.suppliers import (
    PlanSupplier, MemoryPlanSupplier,
    MigrationSupplier, MemoryMigrationSupplier,
    TenantSupplier, MemoryTenantSupplier)
from mediark.application.operation.managers import (
    SetupManager)


@fixture
def plan_supplier() -> PlanSupplier:
    return MemoryPlanSupplier()


@fixture
def migration_supplier() -> MigrationSupplier:
    return MemoryMigrationSupplier()


@fixture
def setup_manager(
    plan_supplier,
    migration_supplier
) -> SetupManager:
    return SetupManager(
        plan_supplier, migration_supplier)


def test_setup_manager_instantiation(setup_manager) -> None:
    assert hasattr(setup_manager, 'prepare')


async def test_setup_manager_prepare(setup_manager) -> None:
    await setup_manager.prepare({})

    assert setup_manager.migration_supplier._migrated
    assert setup_manager.plan_supplier._setup
