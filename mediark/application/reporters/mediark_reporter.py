from abc import ABC, abstractmethod
from ..repositories import ImageRepository, AudioRepository
from .types import ImageDictList, AudioDictList, SearchDomain


class MediarkReporter(ABC):

    @abstractmethod
    async def search_images(self, domain: SearchDomain) -> ImageDictList:
        """Search Mediark's Images"""

    @abstractmethod
    async def search_audios(self, domain: SearchDomain) -> AudioDictList:
        """Search Mediark's Audios"""


class StandardMediarkReporter(MediarkReporter):

    def __init__(self, image_repository: ImageRepository,
                 audio_repository: AudioRepository) -> None:
        self.image_repository = image_repository
        self.audio_repository = audio_repository

    async def search_images(self, domain: SearchDomain) -> ImageDictList:
        return [vars(image) for image in
                (await self.image_repository.search(domain))]

    async def search_audios(self, domain: SearchDomain) -> AudioDictList:
        return [vars(audio) for audio in
                (await self.audio_repository.search(domain))]
