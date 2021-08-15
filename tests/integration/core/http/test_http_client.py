from os import name
from mediark.integration.core.http import HttpClientSupplier
from pytest import fixture, raises
from mediark.integration.core.http import http_client


@fixture
def mock_http_client(monkeypatch):
    class MockClientSession:
        def __init__(self) -> None:
            self.value = None

        async def get(self, url):
            self.value = url
            return ''

    monkeypatch.setattr(http_client, 'ClientSession', MockClientSession)


async def test_http_client(mock_http_client):

    http_client_supplier = HttpClientSupplier()
    await http_client_supplier.get('https://www.google.com')
    await http_client_supplier.get('https://www.google.com')

    assert http_client_supplier.value == 'https://www.google.com'
