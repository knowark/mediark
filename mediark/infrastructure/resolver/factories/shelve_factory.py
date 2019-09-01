from pathlib import Path
from ....application.utilities.query_parser import QueryParser
from ....infrastructure.data import (
    ShelveImageRepository, ShelveAudioRepository)
from ...config import Config
from .memory_factory import MemoryFactory


class ShelveFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def shelve_image_repository(self, query_parser: QueryParser
                                ) -> ShelveImageRepository:
        filename = self.config['shelve'] + self.config['images']['shelve']
        return ShelveImageRepository(query_parser, filename)

    def shelve_audio_repository(self, query_parser: QueryParser
                                ) -> ShelveAudioRepository:
        filename = self.config['shelve'] + self.config['audios']['shelve']
        return ShelveAudioRepository(query_parser, filename)
