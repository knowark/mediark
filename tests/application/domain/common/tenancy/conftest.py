from pytest import fixture
from mediark.application.domain.common import (
    TenantProvider, StandardTenantProvider)


@fixture
def tenant_provider() -> TenantProvider:
    return StandardTenantProvider()
