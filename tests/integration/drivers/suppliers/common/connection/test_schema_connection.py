from pytest import fixture
from mediark.integration.drivers.suppliers import (
    SchemaConnection)
from mediark.integration.drivers.suppliers.common.connection import (
    schema_connection as schema_connection_module)


@fixture
def driver_connection(monkeypatch):
    class MockDriverCursor:
        def __init__(self, dsn):
            self.dsn = dsn
            self.committed = False
            self.closed = False

        def execute(self, query, params):
            self.execute_query = query
            self.execute_params = params

        def fetchall(self):
            return []

        def close(self):
            self.closed = True

    class MockDriverConnection:
        def __init__(self, dsn):
            self.dsn = dsn
            self._cursor = None
            self.committed = False
            self.closed = False

        def cursor(self):
            if not self._cursor:
                self._cursor = MockDriverCursor(self.dsn)
            return self._cursor

        def commit(self):
            self.committed = True

        def close(self):
            self.closed = True

    def mock_connect(dsn):
        return MockDriverConnection(dsn)

    monkeypatch.setattr(schema_connection_module, 'connect', mock_connect)


@fixture
def schema_connection(driver_connection):
    dsn = 'postgresql://user:password@localhost/appdb'
    return SchemaConnection(dsn)


def test_schema_connection_instantiation(schema_connection):
    assert schema_connection is not None


def test_schema_connection_open(schema_connection):
    schema_connection.open()
    assert schema_connection.connection.dsn == 'localhost:appdb:user:password'


def test_schema_connection_close(schema_connection):
    schema_connection.close()
    assert schema_connection.connection is None
    schema_connection.open()
    schema_connection.close()
    assert schema_connection.connection.closed is True
    assert schema_connection.connection.committed is True


def test_schema_connection_execute(schema_connection):
    query = 'INSERT INTO table VALUES (%s)'
    params = ['value']
    schema_connection.execute(query, params)
    assert schema_connection.connection is None
    schema_connection.open()
    schema_connection.execute(query, params)
    assert schema_connection.connection._cursor.execute_query == query
    assert schema_connection.connection._cursor.execute_params == tuple(params)


def test_schema_connection_select(schema_connection):
    query = 'SELECT * FROM table;'
    schema_connection.select(query)
    assert schema_connection.connection is None
    schema_connection.open()
    schema_connection.select(query)
    assert schema_connection.connection._cursor.execute_query == query
    assert schema_connection.connection._cursor.execute_params == ()
