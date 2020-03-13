from abc import ABC, abstractmethod
from ..repositories import MediaRepository
from .types import MediaDictList, SearchDomain


class MediarkReporter(ABC):

    @abstractmethod
    async def search_media(self, domain: SearchDomain) -> MediaDictList:
        """Search Mediark's Media"""


class StandardMediarkReporter(MediarkReporter):

    def __init__(self, media_repository: MediaRepository) -> None:
        self.media_repository = media_repository

    async def search_media(self, domain: SearchDomain) -> MediaDictList:
        return [vars(media) for media in
                (await self.media_repository.search(domain))]
