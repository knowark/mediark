import uuid
from abc import ABC, abstractmethod
from .file_store_service import FileStoreService


class MemoryFileStoreService(FileStoreService):
    def __init__(self):
        self.files = {}

    def store(self, locator: str, content: str, extension: str = None) -> str:
        self.files[locator] = content
        return locator
