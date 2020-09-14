from pathlib import Path
from ...application.models import Media
from ...application.repositories import (
    MediaRepository, MemoryMediaRepository)
from ...application.utilities import (
    QueryParser, TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from ..config import Config
from ..core import TenantSupplier, MemoryTenantSupplier
from .http_factory import HttpFactory


class CheckFactory(HttpFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def check_tenant_supplier(self) -> MemoryTenantSupplier:
        tenant_supplier = MemoryTenantSupplier()
        tenant_supplier.create_tenant({
            'id': '001',
            'name': 'Default',
            'zone': 'default'
        })
        return tenant_supplier

    def check_media_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MemoryMediaRepository:
        media_repository = MemoryMediaRepository(
            query_parser, tenant_provider, auth_provider)
        media_repository.load({
            "default": {
                "1": Media(id='1', reference='ref_1',  uri='value_1'),
                "2": Media(id='2', reference='ref_2', uri='value_2'),
                "3": Media(id='3', reference='ref_3', uri='value_3')
            }
        })
        return media_repository
