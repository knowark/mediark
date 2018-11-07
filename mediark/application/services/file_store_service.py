import uuid
from abc import ABC, abstractmethod


class FileStoreService(ABC):
    @abstractmethod
    def store(self, locator: str, content: str) -> str:
        "Store method to be implemented."


class MemoryFileStoreService(FileStoreService):
    def __init__(self):
        self.files = {}

    def store(self, locator: str, content: str) -> str:
        self.files[locator] = content
        return locator
