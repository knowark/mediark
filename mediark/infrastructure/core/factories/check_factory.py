from pathlib import Path
from ....application.models import (Image, Audio)
from ....application.repositories import (
    ImageRepository, MemoryImageRepository,
    AudioRepository, MemoryAudioRepository)
from ....application.utilities import (
    QueryParser, TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from ..configuration import Config
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from .memory_factory import MemoryFactory


class CheckFactory(MemoryFactory):
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

    def check_image_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MemoryImageRepository:
        image_repository = MemoryImageRepository(
            query_parser, tenant_provider, auth_provider)
        image_repository.load({
            "default": {
                "1": Image(id='1', reference='ref 1',  uri='value_1'),
                "2": Image(id='2', reference='ref 2', uri='value_2'),
                "3": Image(id='3', reference='ref 3', uri='value_3')
            }
        })
        return image_repository

    def check_audio_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MemoryAudioRepository:
        audio_repository = MemoryAudioRepository(
            query_parser, tenant_provider, auth_provider)
        audio_repository.load({
            "default": {
                "1": Audio(id='1', reference='ref 1',  uri='value_1'),
                "2": Audio(id='2', reference='ref 2', uri='value_2')
            }
        })
        return audio_repository
