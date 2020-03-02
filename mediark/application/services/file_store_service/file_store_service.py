from abc import ABC, abstractmethod


class FileStoreService(ABC):
    @abstractmethod
    async def store(
            self, file_id: str, content: str, extension: str = None) -> str:
        "Store method to be implemented."
