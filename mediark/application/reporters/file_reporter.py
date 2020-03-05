from abc import ABC, abstractmethod
from typing import Dict, Any
from ..repositories import ImageRepository, AudioRepository
from ..services import FileStoreService
from .types import ImageDictList, AudioDictList, SearchDomain


class FileReporter(ABC):
    @abstractmethod
    async def load(self, uri: str) -> Dict[str, Any]:
        """Load file from it's location"""


class StandardFileReporter(FileReporter):
    def __init__(self, file_store_service: FileStoreService) -> None:
        self.file_store_service = file_store_service

    async def load(self, uri: str) -> Dict[str, Any]:
        content, context = await self.file_store_service.load(uri)

        print('context:::', context)

        return {'content': content, **context}
