from ..application.domain.models import Media
from ..application.domain.repositories import (
    MediaRepository, MemoryMediaRepository)
from ..application.domain.common import (
    QueryParser, TenantProvider, AuthProvider)
from ..core import Config
from ..core.suppliers.common.tenancy import (
    TenantSupplier, MemoryTenantSupplier)
from .http_factory import HttpFactory


class CheckFactory(HttpFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def tenant_supplier(self) -> TenantSupplier:
        tenant_supplier = MemoryTenantSupplier()
        tenant_supplier.ensure_tenant({
            'id': '001',
            'name': 'Default',
        })
        return tenant_supplier

    def media_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MediaRepository:
        media_repository = MemoryMediaRepository(
            query_parser, tenant_provider, auth_provider)
        media_repository.load({
            "default": {
                '1': Media(
                    **{'id': '1', 'reference': 'ref_1', 'uri': 'value_1'}
                ),
                '2': Media(
                    **{'id': '2', 'reference': 'ref_2', 'uri': 'value_2'}
                ),
                '3': Media(
                    **{'id': '3', 'reference': 'ref_3', 'uri': 'value_3'}
                )
            }
        })
        return media_repository
