from pytest import fixture
from mediark.application.utilities import (
    TenantProvider, StandardTenantProvider)


@fixture
def tenant_provider() -> TenantProvider:
    return StandardTenantProvider()
