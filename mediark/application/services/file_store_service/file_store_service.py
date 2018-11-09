from abc import ABC, abstractmethod


class FileStoreService(ABC):
    @abstractmethod
    def store(self, locator: str, content: str, extension: str = None) -> str:
        "Store method to be implemented."
