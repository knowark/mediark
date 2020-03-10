from pytest import fixture
from json import dump, loads
from pathlib import Path
from mediark.infrastructure.core.tenancy import JsonTenantSupplier


@fixture
def catalog_path(tmp_path):
    catalog_path = str(tmp_path / "tenants.json")
    with open(catalog_path, 'w') as f:
        dump({"tenants": {}}, f, indent=2)
    return catalog_path


@fixture
def directory_data(tmp_path):
    return tmp_path


@fixture
def directory_template(tmp_path):
    template_path = tmp_path / "__template__"

    Path.mkdir(template_path)

    data = ["credentials", "dominions", "errors", "grants", "permissions",
            "policies", "rankings", "resources", "roles", "tokens", "types",
            "users"]

    for model in data:
        with open(template_path / f"{model}.json", 'w') as f:
            dump({model: {}}, f, indent=2)

    return "__template__"


@fixture
def tenant_dict():
    return {
        "id": "c5934df0-cab9-4660-af14-c95272a92ab7",
        "name": "Servagro",
        "email": "",
        "active": True,
        "slug": "servagro",
        "attributes": {},
        "data": {
            "directory": {
                "default": "/home/jjalvarez/data"
            },
            "schema": {
                "default": "postgresql://shiftark:shiftark@localhost/shiftark"
            }
        }
    }


@fixture
def json_tenant_supplier(catalog_path, directory_data, directory_template):
    return JsonTenantSupplier(
        str(catalog_path), str(directory_data), directory_template)

