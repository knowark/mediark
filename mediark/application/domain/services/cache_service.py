import time
import collections
from abc import ABC, abstractmethod
from ..common import TenantProvider


class CacheService(ABC):
    @abstractmethod
    def get(self, key: str, default=None) -> str:
        "Get method to be implemented."

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        "Set method to be implemented."


class StandardCacheService(CacheService):
    """In-memory cache service using an OrderedDict."""

    def __init__(self, tenant_provider: TenantProvider,
                 size=1024, lifetime=300) -> None:
        self.tenant_provider = tenant_provider
        self.size = size
        self.lifetime = lifetime
        self.cache = collections.OrderedDict()

    def get(self, key: str, default=None) -> str:
        key = self._namespace(key)
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
        key = self._namespace(key)
        expiration = time.time() + self.lifetime
        self.cache[key] = (value, expiration)
        self.cache.move_to_end(key)
        if len(self.cache) > self.size:
            self.cache.popitem(last=False)

    def _namespace(self, key: str) -> str:
        return f'{self.tenant_provider.tenant.slug}/{key}'
