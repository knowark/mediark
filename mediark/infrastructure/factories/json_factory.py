from pathlib import Path
from ...application.utilities import QueryParser
from ...infrastructure.data import (
    JsonAudioRepository, JsonImageRepository)
from mediark.application.utilities import TenantProvider, AuthProvider
from ..core import Config, JsonTenantSupplier, TenantSupplier
from .http_factory import HttpFactory


class JsonFactory(HttpFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def json_tenant_supplier(self) -> TenantSupplier:
        catalog_path = self.config['tenancy']['json']
        directory_data = self.config['data']['dir_path']
        return JsonTenantSupplier(catalog_path, directory_data)

    def json_image_repository(
        self, query_parser: QueryParser, tenant_provider: TenantProvider,
        auth_provider: AuthProvider
    ) -> JsonImageRepository:
        return JsonImageRepository(
            query_parser, tenant_provider, auth_provider, 'images')

    def json_audio_repository(
        self, query_parser: QueryParser, tenant_provider: TenantProvider,
        auth_provider: AuthProvider
    ) -> JsonAudioRepository:
        return JsonAudioRepository(
            query_parser, tenant_provider, auth_provider, 'audios')
