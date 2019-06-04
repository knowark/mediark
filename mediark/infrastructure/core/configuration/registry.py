from abc import ABC, abstractmethod
from pathlib import Path
from ...application.repositories import (
    MemoryAudioRepository, MemoryImageRepository, MemoryAudioRepository)
from ...application.utilities.expression_parser import ExpressionParser 
from ...application.services import (StandardIdService, MemoryFileStoreService,
                                     FileStoreService)
from ...application.coordinators import (
    AudioStorageCoordinator, ImageStorageCoordinator)
from ...application.reporters import StandardMediarkReporter
from .config import Config


class Registry(dict, ABC):
    @abstractmethod
    def __init__(self, config: Config) -> None:
        pass


class MemoryRegistry(Registry):

    def __init__(self, config: Config) -> None:
        super().__init__(config)

        parser = ExpressionParser()
        audio_repository = MemoryAudioRepository(parser)
        image_repository = MemoryImageRepository(parser)

        id_service = StandardIdService()
        memory_file_store_service = MemoryFileStoreService()

        audio_storage_coordinator = AudioStorageCoordinator(
            id_service, audio_repository, memory_file_store_service)

        image_storage_coordinator = ImageStorageCoordinator(
            id_service, image_repository, memory_file_store_service)

        mediark_informer = StandardMediarkReporter(image_repository,
                                                   audio_repository)

        self['audio_storage_coordinator'] = audio_storage_coordinator
        self['image_storage_coordinator'] = image_storage_coordinator
        self['mediark_informer'] = mediark_informer


class ProductionRegistry(Registry):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        memory_registry = MemoryRegistry(config)

        self.update(memory_registry)

        audio_storage_coordinator = memory_registry[
            'audio_storage_coordinator']

        image_storage_coordinator = memory_registry[
            'image_storage_coordinator']

        self['audio_storage_coordinator'] = audio_storage_coordinator
        self['image_storage_coordinator'] = image_storage_coordinator
