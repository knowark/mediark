import json
from pathlib import Path
from pytest import fixture
from typing import Dict, Any
from mediark.infrastructure.core.setup import schema_setup_supplier
from mediark.infrastructure.core import SchemaSetupSupplier


def test_schema_setup_supplier_setup(monkeypatch):
    expected = {}

    def mock_sql_migrate(database_uri, migrations_path,
                         schema, target_version):
        nonlocal expected
        expected = {
            "database_uri": database_uri,
            "migrations_path": migrations_path,
            "schema": schema,
            "target_version": target_version
        }
        return None

    monkeypatch.setattr(
        schema_setup_supplier,  'sql_migrate', mock_sql_migrate)

    zones = {
        'default': {
            'dsn': "postgresql://mediark:mediark@localhost/postgres"
        }
    }

    setup_supplier = SchemaSetupSupplier(zones)

    setup_supplier.setup()

    assert len(expected) == 4
    for key, value in expected.items():
        assert value
