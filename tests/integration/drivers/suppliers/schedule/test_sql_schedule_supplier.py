from pytest import fixture
from mediark.application.general.connector import MemoryConnector
from mediark.integration.drivers.suppliers import SqlPlanSupplier


class MockScheduler:
    async def setup(self):
        self._setup= True

    async def time(self):
        self._time = True

    async def work(self):
        self._work = True

    async def defer(self, job, data):
        self._job = job
        self._data = data


@fixture
def connector():
    return MemoryConnector()


async def test_sql_plan_supplier_instantiation(connector):
    plan_supplier = SqlPlanSupplier(connector)

    assert plan_supplier is not None


async def test_sql_plan_supplier_setup(connector):
    plan_supplier = SqlPlanSupplier(connector)
    plan_supplier.scheduler = MockScheduler()

    await plan_supplier.setup()

    assert plan_supplier.scheduler._setup is True


async def test_sql_plan_supplier_defer(connector):
    plan_supplier = SqlPlanSupplier(connector)
    plan_supplier.scheduler = MockScheduler()

    await plan_supplier.defer('OneShotJob', {'custom': 'data'})

    assert plan_supplier.scheduler._job == 'OneShotJob'
    assert plan_supplier.scheduler._data == {'custom': 'data'}

