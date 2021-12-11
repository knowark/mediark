from pytest import fixture
from asyncpg import Connection
from mediark.integration.core.data.sql.connector import (
    sql_connector as sql_connector_module)
from mediark.integration.core.data.sql import SqlConnector


@fixture
def connection_database():
    user = 'mediark'
    password = user
    test_database = 'test_connection_database'
    return f'postgresql://{user}:{password}@localhost/{test_database}'


@fixture
def mock_pool(connection_database, monkeypatch):
    class MockTransaction:
        def __init__(self):
            self.started = False
            self.committed = False
            self.rollbacked = False

        async def start(self):
            self.started = True

        async def rollback(self):
            self.rollbacked = True

        async def commit(self):
            self.committed = True

        async def close(self):
            pass

    class MockConnection(Connection):
        def __init__(self):
            self._transaction = None

        def transaction(self):
            if not self._transaction:
                self._transaction = MockTransaction()
            return self._transaction

        async def fetch(self, query, records):
            self.query = query
            self.records = records
            return []
        async def close(self):
            pass

    class MockPool:
        async def acquire(self):
            self.connection = MockConnection()
            return self.connection

        async def release(self, connection):
            self.released = connection

        def get_size(self):
            pass

    async def mock_create_pool(**options):
        return MockPool()

    monkeypatch.setattr(
        sql_connector_module, 'create_pool', mock_create_pool)


@fixture
def sql_connector(connection_database, mock_pool):
    settings = [{
        'name': 'default',
        'dsn': connection_database,
        'max_size': 10
    }]
    return SqlConnector(settings)
