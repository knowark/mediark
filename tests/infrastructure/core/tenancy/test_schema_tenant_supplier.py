import json
from pathlib import Path
from pytest import fixture
from typing import Dict, Any
from mediark.infrastructure.core.tenancy import schema_tenant_supplier
from mediark.infrastructure.core.tenancy import SchemaTenantSupplier


def test_schema_tenant_supplier_instantiation(monkeypatch):
    expected = {}

    def mock_resolve_managers(config: Dict[str, Any]):
        nonlocal expected
        expected = config
        return None, None

    monkeypatch.setattr(
        schema_tenant_supplier,  'resolve_managers', mock_resolve_managers)
    catalog_dsn = "postgresql://mediark:mediark@localhost/postgres"
    zones = {
        'default': "postgresql://mediark:mediark@localhost/postgres"
    }

    tenant_supplier = SchemaTenantSupplier(catalog_dsn, zones)

    isinstance(tenant_supplier, SchemaTenantSupplier)

    assert expected == {
        'cataloguer_kind': 'schema',
        'catalog_dsn': catalog_dsn,
        'provisioner_kind': 'schema',
        'provision_schema_zones': zones
    }
