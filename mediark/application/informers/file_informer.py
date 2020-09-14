from abc import ABC, abstractmethod
from typing import Dict, Any
from ..domain.services import FileStoreService


class FileInformer(ABC):
    @abstractmethod
    async def load(self, uri: str) -> Dict[str, Any]:
        """Load file from it's location"""


class StandardFileInformer(FileInformer):
    def __init__(self, file_store_service: FileStoreService) -> None:
        self.file_store_service = file_store_service

    async def load(self, uri: str) -> Dict[str, Any]:
        content, context = await self.file_store_service.load(uri)
        return {'body': content, **context}
