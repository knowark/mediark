from abc import ABC, abstractmethod
from ..repositories import ImageRepository
from .types import ImageDictList, SearchDomain


class MediarkReporter(ABC):

    @abstractmethod
    def search_images(self, domain: SearchDomain) -> ImageDictList:
        """Search Mediark's Images"""


class MemoryMediarkReporter(MediarkReporter):

    def __init__(self, image_repository: ImageRepository) -> None:
        self.image_repository = image_repository

    def search_images(self, domain: SearchDomain) -> ImageDictList:
        return [vars(image) for image in
                self.image_repository.search(domain)]
