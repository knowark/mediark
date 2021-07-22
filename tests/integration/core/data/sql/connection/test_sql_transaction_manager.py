from typing import Dict, Any
from filtrark import SqlParser, SafeEval
from modelark import Entity, SqlRepository
from pytest import fixture, raises
from mediark.application.domain.common import (
    Tenant, StandardTenantProvider, User, StandardAuthProvider)
from mediark.integration.core.data import SqlTransactionManager


class SampleEntity(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.size = attributes.get('size', 0)


@fixture
def connection_manager(default_connection_manager):
    return default_connection_manager


@fixture
def tenant_provider():
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="Origin"))
    return tenant_provider


@fixture
def transaction_manager(connection_manager, tenant_provider):
    transaction_manager = SqlTransactionManager(
        connection_manager, tenant_provider)
    return transaction_manager


@fixture
def sample_repository(connection_manager, tenant_provider) -> SqlRepository:
    parser = SqlParser(SafeEval())
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(id='001', name='johndoe'))

    sql_repository: SqlRepository = SqlRepository(
        'samples', SampleEntity, connection_manager,
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


def test_transaction_manager_instantiation(transaction_manager):
    assert transaction_manager is not None


async def test_transaction_manager_decorator(
        dummy_manager, sample_repository, transaction_manager):
    uid = '8dce0040-8b72-4bef-b811-98723ea38583'
    sample = dict(id=uid, name='Second', size=20)

    TransactionClass = transaction_manager(dummy_manager)

    await TransactionClass(sample_repository).insert_sample(sample)

    connection_manager = transaction_manager.connection_manager
    connection_string = connection_manager.settings[0]['dsn']
    pool = connection_manager.pools['default']

    assert pool.connection._transaction.started is True
    assert pool.connection._transaction.committed is True
    assert pool.connection._transaction.rollbacked is False


async def test_transaction_manager_decorator_with_rollback(
        dummy_manager, sample_repository, transaction_manager):
    uid = '67adb3f3-736b-4811-a1a9-c41ff505c5a8'
    sample = dict(id=uid, name='Third', size=30)

    TransactionManager = transaction_manager(dummy_manager)

    with raises(Exception):
        result = await TransactionManager(
            sample_repository).failing_insert_sample(sample)

    connection_manager = transaction_manager.connection_manager
    connection_string = connection_manager.settings[0]['dsn']

    pool = connection_manager.pools['default']

    assert pool.connection._transaction.started is True
    assert pool.connection._transaction.committed is False
    assert pool.connection._transaction.rollbacked is True


async def test_transaction_manager_decorator_private_methods(
        dummy_manager, sample_repository, transaction_manager):
    TransactionManager = transaction_manager(dummy_manager)

    result = await TransactionManager(sample_repository)._private_method()

    connection_manager = transaction_manager.connection_manager
    assert result == 'PRIVATE_VALUE'
    assert getattr(connection_manager, 'pools') == {}
