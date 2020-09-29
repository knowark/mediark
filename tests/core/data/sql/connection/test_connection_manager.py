from asyncpg import Connection
from mediark.core.data.sql import  ConnectionManager


def test_connection_manager_methods() -> None:
    methods = ConnectionManager.__abstractmethods__  # type: ignore
    assert 'get' in methods
    assert 'put' in methods


def test_default_connection_manager_instantiation(
        default_connection_manager):
    assert default_connection_manager is not None
    assert len(default_connection_manager.default) > 0


async def test_default_connection_manager_get(
        default_connection_manager):

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
    assert default_connection_manager.pools['default'].released is connection_1
