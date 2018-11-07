from abc import ABC, abstractmethod
from .config import Config
from ...application.repositories import (
    ExpressionParser, MemoryImageRepository)
from ...application.services import StandardIdService
from ...application.coordinators import ImageStorageCoordinator


class Registry(dict, ABC):
    @abstractmethod
    def __init__(self, config: Config) -> None:
        pass


class MemoryRegistry(Registry):

    def __init__(self, config: Config) -> None:
        super().__init__(config)

        parser = ExpressionParser()
        image_repository = MemoryImageRepository(parser)

        id_service = StandardIdService()

        image_storage_coordinator = ImageStorageCoordinator(
            image_repository, id_service)

        self['image_storage_coordinator'] = image_storage_coordinator
