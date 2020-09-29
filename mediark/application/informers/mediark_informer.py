from abc import ABC, abstractmethod
from ..domain.repositories import MediaRepository
from ..domain.common import RecordList, QueryDomain


class MediarkInformer(ABC):

    @abstractmethod
    async def search(self,
                     model: str,
                     domain: QueryDomain = None,
                     limit: int = 0,
                     offset: int = 0) -> RecordList:
        """Returns a list of <<model>> dictionaries matching the domain"""

    @abstractmethod
    async def count(self,
                    model: str,
                    domain: QueryDomain = None) -> int:
        """Returns a the <<model>> records count"""


class StandardMediarkInformer(MediarkInformer):

    def __init__(self, media_repository: MediaRepository) -> None:
        self.media_repository = media_repository

    async def search(self,
                     model: str,
                     domain: QueryDomain = None,
                     limit: int = 10_000,
                     offset: int = 0) -> RecordList:
        repository = getattr(self, f'{model}_repository')
        return [vars(entity) for entity in
                await repository.search(
            domain or [], limit=limit, offset=offset)]

    async def count(self,
                    model: str,
                    domain: QueryDomain = None) -> int:
        repository = getattr(self, f'{model}_repository')
        return await repository.count(domain or [])
