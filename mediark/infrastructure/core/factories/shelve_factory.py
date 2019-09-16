from pathlib import Path
from ....application.utilities import QueryParser
from ....infrastructure.data import (
    ShelveImageRepository, ShelveAudioRepository)
from mediark.application.utilities import TenantProvider
from ..configuration import Config
from .memory_factory import MemoryFactory


class ShelveFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def shelve_image_repository(
        self, query_parser: QueryParser, tenant_provider: TenantProvider
    ) -> ShelveImageRepository:
        return ShelveImageRepository(
            query_parser, tenant_provider, self.config['data'], 'images')

    def shelve_audio_repository(
        self, query_parser: QueryParser, tenant_provider: TenantProvider
    ) -> ShelveAudioRepository:
        filename = self.config['shelve'] + self.config['audios']['shelve']
        return ShelveAudioRepository(
            query_parser, tenant_provider, self.config['data'], 'audios')
