import os
from pathlib import Path
from pytest import fixture
from mediark.infrastructure.data import (
    SwiftAuthSupplier,
    SwiftFileStoreService)
from mediark.infrastructure.core import build_config
from mediark.application.utilities import StandardTenantProvider, Tenant


@fixture
def mock_http_client():
    class MockResponse:
        def __init__(self, headers=None, json=None, content=None):
            self.status = 200
            self.headers = headers
            self._json = json
            self._content = content

        async def read(self):
            return self._content

        async def json(self):
            return self._json

    class MockAuthContextManager:
        async def __aenter__(self):
            return MockResponse(
                headers={'X-Subject-Token': 'AUTH_TOKEN_123'},
                json={'token': {'expires_at': '2999-03-11T00:36:55.0Z'}})

        async def __aexit__(self, *args):
            pass

    class MockUploadContextManager:
        async def __aenter__(self):
            return MockResponse()

        async def __aexit__(self, *args):
            pass

    class MockDownloadContextManager:
        async def __aenter__(self):
            return MockResponse(headers={}, content=b'BINARY_DATA')

        async def __aexit__(self, *args):
            pass

    class MockHttpClient:
        def post(self, url, json):
            return MockAuthContextManager()

        def put(self, url, headers, data):
            return MockUploadContextManager()

        def get(self, url, headers):
            return MockDownloadContextManager()

    return MockHttpClient()


@fixture
def swift_auth_supplier(mock_http_client):
    auth_url = "https://auth.cloud/v3/auth/tokens"
    username = "knowark"
    password = "abcd1234"

    return SwiftAuthSupplier(
        mock_http_client, auth_url, username, password)


@fixture
def swift_file_store_service(swift_auth_supplier, mock_http_client):
    data_config = build_config('', 'DEV')['data']

    standard_tenant_provider = StandardTenantProvider()
    standard_tenant_provider.setup(Tenant(id='2', name="custom-tenant"))
    return SwiftFileStoreService(
        standard_tenant_provider, swift_auth_supplier,
        mock_http_client, data_config)
