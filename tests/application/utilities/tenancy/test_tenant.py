from pytest import fixture, raises
from mediark.application.utilities import (
    TenantLocationError, Tenant, TenantCreationError)


@fixture
def tenant() -> Tenant:
    return Tenant(id='001', name="Amazon")


def test_tenant_creation(tenant: Tenant) -> None:
    assert isinstance(tenant, Tenant)


def test_tenant_default_attributes(tenant: Tenant) -> None:
    assert tenant.id == "001"
    assert tenant.name == "Amazon"
    assert tenant.slug == 'amazon'
    assert tenant.zone == ''


def test_tenant_attributes_from_dict() -> None:

    tenant_dict = {
        "id": "farbo007",
        "name": "Hortofrutícola El Cariño"
    }

    tenant = Tenant(**tenant_dict)

    for key, value in tenant_dict.items():
        assert getattr(tenant, key) == value


def test_tenant_normalize_slug() -> None:
    given_slug = "Hortofrutícola El Cariño"
    slug = Tenant._normalize_slug(given_slug)

    assert slug == 'hortofruticola_el_carino'


def test_tenant_normalize_slug_invalid() -> None:
    empty_slug = "  "
    with raises(TenantCreationError):
        Tenant._normalize_slug(empty_slug)

    unsupported_slug = " あ "
    with raises(TenantCreationError):
        resp = Tenant._normalize_slug(unsupported_slug)
