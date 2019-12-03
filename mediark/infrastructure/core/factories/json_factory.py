from pathlib import Path
from ....application.utilities import QueryParser
from ....infrastructure.data import (
    JsonAudioRepository, JsonImageRepository)
from mediark.application.utilities import TenantProvider, AuthProvider
from ..configuration import Config
from .memory_factory import MemoryFactory


class JsonFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

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
