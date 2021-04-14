import time
import collections
from abc import ABC, abstractmethod


class CacheService(ABC):
    @abstractmethod
    def get(self, key: str, default=None) -> str:
        "Get method to be implemented."

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        "Set method to be implemented."


class StandardCacheService(CacheService):
    """In-memory cache service using an OrderedDict."""

    def __init__(self, size=1024, lifetime=300) -> None:
        self.cache = collections.OrderedDict()
        self.size = size
        self.lifetime = lifetime

    def get(self, key: str, default=None) -> str:
        if key not in self.cache:
            return (default if default is not None
                    else self.cache[key])

        self.cache.move_to_end(key)
        value, expiration = self.cache[key]
        if time.time() < expiration:
            return value

        self.cache.popitem()
        return (default if default is not None
                else self.cache[key])

    def set(self, key: str, value: str) -> None:
        expiration = time.time() + self.lifetime
        self.cache[key] = (value, expiration)
        self.cache.move_to_end(key)
        if len(self.cache) > self.size:
            self.cache.popitem(last=False)
