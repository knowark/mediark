from pathlib import Path
from ...application.repositories import ExpressionParser
from ...infrastructure.data import ShelveImageRepository
from ..config import Config
from .memory_factory import MemoryFactory


class ShelveFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.home = str(Path.home())

    def shelve_image_repository(self, expression_parser: ExpressionParser
                                ) -> ShelveImageRepository:
        filename = self.home + '/images.db'
        return ShelveImageRepository(expression_parser, filename)
