from abc import ABC, abstractmethod
from ..domain.repositories import MediaRepository
from ..domain.models import Media
from .types import MediaDictList, QueryDomain


class MediarkInformer(ABC):

    @abstractmethod
    async def search_media(self,
                           model: str,
                           # domain: SearchDomain,
                           domain: QueryDomain,
                           limit: int = 0,
                           offset: int = 0) -> MediaDictList:
        """Search Mediark's Media"""


class StandardMediarkInformer(MediarkInformer):

    def __init__(self, media_repository: MediaRepository) -> None:
        self.media_repository = media_repository

    async def search_media(self,
                           model: str,
                           # domain: SearchDomain,
                           domain: QueryDomain,
                           limit: int = 1000,
                           offset: int = 0) -> MediaDictList:
        repository = getattr(self, f'{model}_repository')
        return [vars(entity) for entity in
                await repository.search(
                domain or [], limit=limit, offset=offset)]
        # return [vars(media) for media in
        #         (await self.media_repository.search(domain))]
