from pytest import fixture, raises
from asyncpg import Connection
from mediark.infrastructure.data.sql import (
    ConnectionManager,
    DefaultConnectionManager)


def test_connection_manager_methods() -> None:
    methods = ConnectionManager.__abstractmethods__  # type: ignore
    assert 'get' in methods
    assert 'put' in methods


@fixture
def default_connection_manager(connection_database):
    settings = [{
        'name': 'default',
        'dsn': connection_database,
        'max_size': 10
    }]
    connection_manager = DefaultConnectionManager(settings)
    return connection_manager


def test_default_connection_manager_instantiation(
        default_connection_manager):
    assert default_connection_manager is not None
    assert len(default_connection_manager.default) > 0


async def test_default_connection_manager_get(default_connection_manager):
    connection = await default_connection_manager.get()
    assert connection is not None
    assert isinstance(connection, Connection)


async def test_default_connection_manager_get_repeated(
        default_connection_manager):
    connection_1 = await default_connection_manager.get()
    connection_2 = await default_connection_manager.get()
    assert connection_1 is connection_2


async def test_default_connection_manager_put(default_connection_manager):
    connection_1 = await default_connection_manager.get()

    await default_connection_manager.put(connection_1)

    connection_2 = await default_connection_manager.get()
    assert connection_1 is not connection_2
