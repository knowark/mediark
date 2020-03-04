import inspect
import psycopg2
import rapidjson as json
from typing import Dict, Any
from filtrark import SqlParser, SafeEval
from pytest import fixture, raises
from asyncpg import connect
from mediark.application.utilities import (
    Tenant, StandardTenantProvider, User, StandardAuthProvider)
from mediark.application.models import Entity
from mediark.infrastructure.data import (
    ConnectionManager, DefaultConnectionManager,
    SqlTransactionManager, SqlRepository)


class SampleEntity(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.size = attributes.get('size', 0)


@fixture(scope='session')
def schema(connection_database):
    user = 'mediark'
    password = user

    schema = 'origin'
    connection = psycopg2.connect(connection_database)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {schema};')
    connection.close()

    return schema


@fixture(scope='session')
def samples_table(connection_database, schema):
    connection = psycopg2.connect(connection_database)
    connection.autocommit = True
    table = 'samples'

    uid_1 = '99cc4dc3-4a6e-43a6-ae5f-1c126bf7c0c6'
    data_1 = json.dumps({
        'id': uid_1,
        'name': 'First',
        'size': '10'
    })

    with connection.cursor() as cursor:
        cursor.execute(
            f"CREATE TABLE {schema}.{table} ("
            "data JSONB)")
        cursor.execute(
            f"CREATE UNIQUE INDEX IF NOT EXISTS pk_{table}_id ON "
            f"{schema}.{table} ((data ->> 'id'));")

    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {schema}.{table} "
            "(data) "
            "VALUES (%s)", (data_1,))

    connection.close()
    return table


@fixture
def connection_manager(connection_database):
    return DefaultConnectionManager(settings=[{
        'name': 'default',
        'dsn': connection_database,
        'max_size': 10
    }])


@fixture
def tenant_provider():
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id="001", name="Origin"))
    return tenant_provider


@fixture
def transaction_manager(connection_manager, tenant_provider):
    transaction_manager = SqlTransactionManager(
        connection_manager, tenant_provider)
    return transaction_manager


@fixture
def sample_repository(connection_manager, tenant_provider, samples_table
                      ) -> SqlRepository:
    parser = SqlParser(SafeEval())
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(id='001', name='johndoe'))

    sql_repository: SqlRepository = SqlRepository(
        table=samples_table,
        constructor=SampleEntity,
        tenant_provider=tenant_provider,
        auth_provider=auth_provider,
        connection_manager=connection_manager,
        parser=parser)

    return sql_repository


@fixture
def dummy_coordinator():

    class DummyCoordinator:
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

    return DummyCoordinator


def test_transaction_manager_instantiation(transaction_manager):
    assert transaction_manager is not None


async def test_transaction_manager_decorator(
        dummy_coordinator, sample_repository, transaction_manager):
    uid = '8dce0040-8b72-4bef-b811-98723ea38583'
    sample = dict(id=uid, name='Second', size=20)

    TransactionCoordinator = transaction_manager(dummy_coordinator)

    await TransactionCoordinator(sample_repository).insert_sample(sample)

    connection_manager = transaction_manager.connection_manager
    connection_string = connection_manager.settings[0]['dsn']
    connection = await connect(connection_string)
    async with connection.transaction():
        result = await connection.fetch(
            f"SELECT data FROM origin.samples")

    assert len(result) == 2
    assert any(json.loads(item['data'])['id'] == uid for item in result)


async def test_transaction_manager_decorator_with_rollback(
        dummy_coordinator, sample_repository, transaction_manager):
    uid = '67adb3f3-736b-4811-a1a9-c41ff505c5a8'
    sample = dict(id=uid, name='Third', size=30)

    TransactionCoordinator = transaction_manager(dummy_coordinator)

    with raises(Exception):
        result = await TransactionCoordinator(
            sample_repository).failing_insert_sample(sample)

    connection_manager = transaction_manager.connection_manager
    connection_string = connection_manager.settings[0]['dsn']
    connection = await connect(connection_string)
    async with connection.transaction():
        result = await connection.fetch(
            f"SELECT data FROM origin.samples")

    assert not any(json.loads(item['data'])['id'] == uid for item in result)
