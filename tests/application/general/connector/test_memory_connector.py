from pytest import fixture
from mediark.application.general.connector import (
    MemoryConnection, MemoryConnector, MemoryTransactor)


def test_memory_connection_instantiation():
    connection = MemoryConnection()

    assert connection is not None


async def test_memory_connection_fetch():
    fetch_results = [[{'given': 'result'}]]

    connection = MemoryConnection(fetch_results=fetch_results)

    query = 'SOME PERSISTANCE SERVICE QUERY'
    parameters = ('A', 'B', 'C')

    result = await connection.fetch(query, *parameters)

    assert result == [{'given': 'result'}]
    assert connection.fetch_arguments == [(query, parameters, {})]


async def test_memory_connection_execute():
    execute_results = ['RESULT']

    connection = MemoryConnection(execute_results=execute_results)

    query = 'SOME PERSISTANCE SERVICE QUERY'
    parameters = ('A', 'B', 'C')

    async with connection.transaction():
        result = await connection.execute(query, *parameters)

    assert result == 'RESULT'
    assert connection.execute_arguments == [(query, parameters, {})]


async def test_memory_connector_get_and_put():
    connector = MemoryConnector()
    connection = await connector.get()
    await connector.put(connection)
    assert isinstance(connection, MemoryConnection)


async def test_memory_transactor_call():
    class MockManager:
        pass

    transactor = MemoryTransactor()
    manager = transactor(MockManager)

    assert manager is MockManager
    assert transactor.transactionless(manager) == []
