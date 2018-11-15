from pathlib import Path
from ....application.repositories import ExpressionParser
from ....infrastructure.data import (
    ShelveImageRepository, ShelveAudioRepository)
from ...config import Config
from .memory_factory import MemoryFactory


class ShelveFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def shelve_image_repository(self, expression_parser: ExpressionParser
                                ) -> ShelveImageRepository:
        filename = self.config['shelve'] + self.config['images']['shelve']
        return ShelveImageRepository(expression_parser, filename)

    def shelve_audio_repository(self, expression_parser: ExpressionParser
                                ) -> ShelveAudioRepository:
        filename = self.config['shelve'] + self.config['audios']['shelve']
        return ShelveAudioRepository(expression_parser, filename)
