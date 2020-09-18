from abc import ABC, abstractmethod
from typing import Dict, Any
from ..domain.services import FileStoreService
from mediark.application.domain.common import QueryDomain


class FileInformer(ABC):
    @abstractmethod
    async def load(self,
                   uri: str,
                   domain: QueryDomain = None,
                   limit: int = 0,
                   offset: int = 0) -> Dict[str, Any]:
        """Returns a list of <<model>> dictionaries matching the domain"""


class StandardFileInformer(FileInformer):
    def __init__(self, file_store_service: FileStoreService) -> None:
        self.file_store_service = file_store_service

    async def load(self,
                   uri: str,
                   domain: QueryDomain = None,
                   limit: int = 0,
                   offset: int = 0) -> Dict[str, Any]:
        content, context = await self.file_store_service.load(uri)
        return {'body': content, **context}

