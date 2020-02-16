from pytest import fixture, raises
from psycopg2 import OperationalError
from mediark.infrastructure.data.sql import gevent_wait_callback


def test_connection_callback() -> None:
    assert gevent_wait_callback is not None


def test_connection_callback_operational_error() -> None:
    class MockConnection:
        def poll(self):
            return "BAD_STATE"

    with raises(OperationalError):
        gevent_wait_callback(MockConnection())
