from pytest import fixture
from asyncpg import Connection
from mediark.core.data.sql.connection import connection_manager
from mediark.core.data.sql import DefaultConnectionManager


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

    class MockPool:
        async def acquire(self):
            self.connection = MockConnection()
            return self.connection

        async def release(self, connection):
            self.released = connection

    async def mock_create_pool(**options):
        return MockPool()
    monkeypatch.setattr(connection_manager, 'create_pool', mock_create_pool)


@fixture
def default_connection_manager(connection_database, mock_pool):
    settings = [{
        'name': 'default',
        'dsn': connection_database,
        'max_size': 10
    }]
    return DefaultConnectionManager(settings)
