import json
from mediark.infrastructure.core.tenancy import JsonTenantSupplier
from pathlib import Path


def test_json_tenant_supplier_instantiation(json_tenant_supplier):
    isinstance(json_tenant_supplier, JsonTenantSupplier)


def test_json_tenant_supplier_tenant_creation(
        json_tenant_supplier, tenant_dict, directory_data):
    json_tenant_supplier.create_tenant(tenant_dict)

    with open(directory_data / "tenants.json", 'r') as catalog:
        data = catalog.read()

    catalog_data = json.loads(data)

    assert len(catalog_data["tenants"]) == 1


def test_json_tenant_supplier_get_tenant(
        json_tenant_supplier, tenant_dict, directory_data):
    json_tenant_supplier.create_tenant(tenant_dict)
    tenant = json_tenant_supplier.get_tenant(tenant_dict["id"])

    assert tenant["id"] == tenant_dict["id"]


def test_json_tenant_supplier_search_tenants(
        json_tenant_supplier, tenant_dict, directory_data):
    json_tenant_supplier.create_tenant(tenant_dict)
    tenants = json_tenant_supplier.search_tenants("")

    assert len(tenants) == 1


def test_json_tenant_supplier_resolve_tenant(
        json_tenant_supplier, tenant_dict, directory_data):
    json_tenant_supplier.create_tenant(tenant_dict)
    tenant = json_tenant_supplier.resolve_tenant('Servagro')

    assert tenant['slug'] == 'servagro'
