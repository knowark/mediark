from time import strptime
from mediark.integration.core.suppliers import SwiftAuthSupplier
from mediark.integration.core.suppliers.cloud.swift.swift_auth_supplier import time


def test_swift_auth_supplier_instantiation(swift_auth_supplier):
    assert isinstance(swift_auth_supplier, SwiftAuthSupplier)


async def test_swift_auth_supplier_authenticate(swift_auth_supplier):
    token = await swift_auth_supplier.authenticate()
    assert token == 'AUTH_TOKEN_123'


async def test_swift_auth_supplier_cached_token(
        swift_auth_supplier, monkeypatch):

    def mock_gmtime():
        return strptime("2020-03-10", "%Y-%m-%d")

    monkeypatch.setattr(time, 'gmtime', mock_gmtime)

    swift_auth_supplier.token = 'CACHED_TOKEN'
    swift_auth_supplier.expires_at = strptime("2020-03-11", "%Y-%m-%d")
    token = await swift_auth_supplier.authenticate()

    assert token == 'CACHED_TOKEN'


def test_swift_auth_supplier_make_request(swift_auth_supplier):
    assert swift_auth_supplier._make_request() == {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": "knowark",
                        "domain": {
                            "name": "Default"
                        },
                        "password": "abcd1234"
                    }
                }
            }
        }
    }
