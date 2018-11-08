from ...application.repositories import (
    ExpressionParser,  ImageRepository, MemoryImageRepository)
from ...application.services import (
    IdService, StandardIdService)
from ...application.coordinators import ImageStorageCoordinator
from ...application.reporters import MediarkReporter, MemoryMediarkReporter
from ..config import Config


class MemoryFactory:
    def __init__(self, config: Config) -> None:
        self.config = config

    def expression_parser(self) -> ExpressionParser:
        return ExpressionParser()

    def standard_id_service(self) -> StandardIdService:
        return StandardIdService()

    def memory_image_repository(self, expression_parser: ExpressionParser
                                ) -> MemoryImageRepository:
        return MemoryImageRepository(expression_parser)

    def image_storage_coordinator(self, image_repository: ImageRepository,
                                  id_service: IdService
                                  ) -> ImageStorageCoordinator:
        return ImageStorageCoordinator(image_repository, id_service)

    def memory_mediark_repository(self, image_repository: ImageRepository
                                  ) -> MemoryMediarkReporter:
        return MemoryMediarkReporter(image_repository)


PROVIDERS = {
    "ExpressionParser": {
        "method": "expression_parser"
    },
    "IdService": {
        "method": "standard_id_service"
    },
    "ImageRepository": {
        "method": "memory_image_repository",
        "dependencies": ["ExpressionParser"]
    },
    "ImageStorageCoordinator": {
        "method": "image_storage_coordinator",
        "dependencies": ["ImageRepository", "IdService"]
    },
    "MediarkRepository": {
        "method": "memory_mediark_repository",
        "dependencies": ["ImageRepository"]
    }
}
