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
        headers = {'X-Subject-Token': 'AUTH_TOKEN_123'}

        async def json(self):
            return {'token': {'expires_at': '2999-03-11T00:36:55.0Z'}}

    class MockContextManager:
        async def __aenter__(self):
            return MockResponse()

        async def __aexit__(self, *args):
            pass

    class MockHttpClient:
        def post(self, url, json):
            return MockContextManager()

    return MockHttpClient()


@fixture
def swift_auth_supplier(mock_http_client):
    auth_url = "https://auth.cloud/v3/auth/tokens"
    username = "knowark"
    password = "abcd1234"

    return SwiftAuthSupplier(
        mock_http_client, auth_url, username, password)


@fixture
def swift_file_store_service(tmp_path):
    config = build_config('DEV')['data']
    config['dir_path'] = tmp_path / 'data'
    standard_tenant_provider = StandardTenantProvider()
    standard_tenant_provider.setup(Tenant(id='2', name="custom-tenant"))
    return SwiftFileStoreService(
        standard_tenant_provider, config,
        'images', 'png')
