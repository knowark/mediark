from typing import Dict, Any
from pytest import fixture, raises
from asyncpg import Connection
from modelark import Entity, SqlRepository, SafeEval, SqlParser
from mediark.application.domain.common import (
    Tenant, StandardTenantProvider, User, StandardAuthProvider)
from mediark.application.general.connector import (
    Connector)
from mediark.integration.core.data import (
    SqlConnector, SqlTransactor)


def test_connector_methods() -> None:
    methods = Connector.__abstractmethods__  # type: ignore
    assert 'get' in methods
    assert 'put' in methods


def test_sql_connector_instantiation(
        sql_connector):
    assert sql_connector is not None
    assert len(sql_connector.default) > 0


async def test_sql_connector_get(
        sql_connector):

    connection = await sql_connector.get()
    assert connection is not None
    assert isinstance(connection, Connection)


async def test_sql_connector_get_repeated(
        sql_connector):
    connection_1 = await sql_connector.get()
    connection_2 = await sql_connector.get()
    assert connection_1 is connection_2


async def test_sql_connector_put(sql_connector):
    connection_1 = await sql_connector.get()

    await sql_connector.put(connection_1)

    connection_2 = await sql_connector.get()
    assert connection_1 is not connection_2
    assert sql_connector.pools['default'].released is connection_1


class SampleEntity(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.size = attributes.get('size', 0)


@fixture
def connector(sql_connector):
    return sql_connector


@fixture
def tenant_provider():
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="Origin"))
    return tenant_provider


@fixture
def sql_transactor(connector, tenant_provider):
    sql_transactor = SqlTransactor(connector, tenant_provider)
    return sql_transactor


@fixture
def sample_repository(connector, tenant_provider) -> SqlRepository:
    parser = SqlParser(SafeEval())
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(id='001', name='johndoe'))

    sql_repository: SqlRepository = SqlRepository(
        'samples', SampleEntity, connector,
        parser, tenant_provider, auth_provider)

    return sql_repository


@fixture
def dummy_manager():
    class DummyManager:
        def __init__(self, sample_repository: SqlRepository) -> None:
            self.sample_repository = sample_repository

        async def insert_sample(
                self, sample_dict: Dict[str, Any]) -> None:
            sample = SampleEntity(**sample_dict)
            await self.sample_repository.add(sample)

        async def failing_insert_sample(
                self, sample_dict: Dict[str, Any]) -> None:
            sample = SampleEntity(**sample_dict)
            await self.sample_repository.add(sample)
            raise Exception('Insertion Error!')

        async def _private_method(self) -> str:
            return 'PRIVATE_VALUE'

    return DummyManager

async def test_sql_connector_get_not_pools(
    connector):

    result = await connector.get('not_pool')

    assert result._transaction == None

def test_sql_transactor_instantiation(sql_transactor):
    assert sql_transactor is not None


async def test_sql_transactor_decorator(
        dummy_manager, sample_repository, sql_transactor):
    uid = '8dce0040-8b72-4bef-b811-98723ea38583'
    sample = dict(id=uid, name='Second', size=20)

    TransactionClass = sql_transactor(dummy_manager)

    await TransactionClass(sample_repository).insert_sample(sample)

    connector = sql_transactor.connector
    connection_string = connector.settings[0]['dsn']
    pool = connector.pools['default']

    assert pool.connection._transaction.started is True
    assert pool.connection._transaction.committed is True
    assert pool.connection._transaction.rollbacked is False


async def test_sql_transactor_decorator_with_rollback(
        dummy_manager, sample_repository, sql_transactor):
    uid = '67adb3f3-736b-4811-a1a9-c41ff505c5a8'
    sample = dict(id=uid, name='Third', size=30)

    Transactor = sql_transactor(dummy_manager)

    with raises(Exception):
        result = await Transactor(
            sample_repository).failing_insert_sample(sample)

    connector = sql_transactor.connector
    connection_string = connector.settings[0]['dsn']

    pool = connector.pools['default']

    assert pool.connection._transaction.started is True
    assert pool.connection._transaction.committed is False
    assert pool.connection._transaction.rollbacked is True


async def test_sql_transactor_decorator_private_methods(
        dummy_manager, sample_repository, sql_transactor):
    Transactor = sql_transactor(dummy_manager)

    result = await Transactor(sample_repository)._private_method()

    connector = sql_transactor.connector
    assert result == 'PRIVATE_VALUE'
    assert getattr(connector, 'pools') == {}
