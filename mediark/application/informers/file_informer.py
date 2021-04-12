from abc import ABC, abstractmethod
from typing import Dict, Any
from ..domain.services import FileStoreService, Writer
from mediark.application.domain.common import QueryDomain


class FileInformer(ABC):
    @abstractmethod
    async def load(self, uri: str, stream: Writer) -> Dict[str, Any]:
        """Loads the uri referenced file into the given write stream"""


class StandardFileInformer(FileInformer):
    def __init__(self, file_store_service: FileStoreService) -> None:
        self.file_store_service = file_store_service

    async def load(self, uri: str, stream: Writer) -> Dict[str, Any]:
        return await self.file_store_service.load(uri, stream)
