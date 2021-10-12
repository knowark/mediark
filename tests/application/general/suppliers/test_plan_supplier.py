from mediark.application.general.suppliers import (
    PlanSupplier, MemoryPlanSupplier)


def test_plan_supplier_methods() -> None:
    methods = PlanSupplier.__abstractmethods__  # type: ignore
    assert 'setup' in methods
    assert 'defer' in methods


async def test_memory_plan_suplier_setup() -> None:
    plan_supplier = MemoryPlanSupplier()

    await plan_supplier.setup()

    assert plan_supplier._setup is True


async def test_memory_plan_suplier_defer() -> None:
    plan_supplier = MemoryPlanSupplier()

    await plan_supplier.defer('DailyJob', {'task': 'data'})

    assert plan_supplier._job == 'DailyJob'
    assert plan_supplier._payload == {'task': 'data'}
