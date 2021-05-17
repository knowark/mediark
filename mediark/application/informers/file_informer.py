from abc import ABC, abstractmethod
from typing import Dict, Any
from ..domain.common import MediaNotFoundError
from ..domain.repositories import MediaRepository
from ..domain.services import FileStoreService, CacheService, Writer
from mediark.application.domain.common import QueryDomain


class FileInformer(ABC):
    @abstractmethod
    async def load(self, uri: str, stream: Writer) -> Dict[str, Any]:
        """Loads the uri referenced file into the given write stream"""


class StandardFileInformer(FileInformer):
    def __init__(self, file_store_service: FileStoreService,
                 media_repository: MediaRepository) -> None:
        self.file_store_service = file_store_service
        self.media_repository = media_repository

    async def load(self, path: str, stream: Writer) -> None:
        media = next(iter(await self.media_repository.search([
            '|', ('path', '=', path), ('uri', '=', path)])), None)
        if not media:
            raise MediaNotFoundError(
                f'No media records where found with path: {path}')

        await stream.setup(vars(media))
        await self.file_store_service.load(media.uri, stream)
