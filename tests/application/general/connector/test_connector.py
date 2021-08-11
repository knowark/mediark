from pytest import fixture
from mediark.application.general.connector import (
    Connector, Connection)


def test_connection_methods():
    methods = dir(Connection)
    assert 'fetch' in methods
    assert 'execute' in methods


def test_connector_methods():
    methods = Connector.__abstractmethods__  # type: ignore
    assert 'get' in methods
    assert 'put' in methods
