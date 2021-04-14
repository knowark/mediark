import collections
from abc import ABC, abstractmethod


class CacheService(ABC):
    @abstractmethod
    def get(self, key: str, default=None) -> str:
        "Get method to be implemented."

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        "Set method to be implemented."


class StandardCacheService(IdService):
    """In-memory cache service using an OrderedDict."""

    def __init__(self) -> None:
        self.cache = OrderedDict()

    def get(self, key: str, default=None) -> str:
        "Get method to be implemented."

    def set(self, key: str, value: str) -> None:
        "Set method to be implemented."
