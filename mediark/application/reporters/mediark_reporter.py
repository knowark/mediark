from abc import ABC, abstractmethod
from ..repositories import MediaRepository, ImageRepository, AudioRepository
from .types import MediaDictList, ImageDictList, AudioDictList, SearchDomain


class MediarkReporter(ABC):

    @abstractmethod
    async def search_media(self, domain: SearchDomain) -> MediaDictList:
        """Search Mediark's Media"""

    @abstractmethod
    async def search_images(self, domain: SearchDomain) -> ImageDictList:
        """Search Mediark's Images"""

    @abstractmethod
    async def search_audios(self, domain: SearchDomain) -> AudioDictList:
        """Search Mediark's Audios"""


class StandardMediarkReporter(MediarkReporter):

    def __init__(self, media_repository: MediaRepository,
                 image_repository: ImageRepository,
                 audio_repository: AudioRepository) -> None:
        self.media_repository = media_repository
        self.image_repository = image_repository
        self.audio_repository = audio_repository

    async def search_media(self, domain: SearchDomain) -> MediaDictList:
        return [vars(media) for media in
                (await self.media_repository.search(domain))]

    async def search_images(self, domain: SearchDomain) -> ImageDictList:
        return [vars(image) for image in
                (await self.image_repository.search(domain))]

    async def search_audios(self, domain: SearchDomain) -> AudioDictList:
        return [vars(audio) for audio in
                (await self.audio_repository.search(domain))]
