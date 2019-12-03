import time
from uuid import uuid4
from collections import defaultdict
from typing import List, Dict, TypeVar, Optional, Type, Generic
from ..models import T
from ..utilities import (
    QueryParser, QueryDomain, EntityNotFoundError,
    TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from .repository import Repository


class MemoryRepository(Repository, Generic[T]):
    def __init__(self,  parser=QueryParser(),
                 tenant_provider=StandardTenantProvider(),
                 auth_provider=StandardAuthProvider()) -> None:
        self.data: Dict[str, Dict[str, T]] = defaultdict(dict)
        self.parser: QueryParser = parser
        self.tenant_provider: TenantProvider = tenant_provider
        self.auth_provider: AuthProvider = auth_provider
        self.max_items = 1000

    def get(self, id: str) -> T:
        item = self.data[self._location].get(id)
        if not item:
            raise EntityNotFoundError(
                f"The entity with id {id} was not found.")
        return item

    def add(self, item: T) -> T:
        user = self.auth_provider.user
        item.id = item.id or str(uuid4())
        item.created_at = int(time.time())
        item.created_by = user and user.id or ""
        item.updated_at = item.created_at
        item.updated_by = item.created_by
        self.data[self._location][item.id] = item
        return item

    def update(self, item: T) -> bool:
        if item.id not in self.data[self._location]:
            return False
        user = self.auth_provider.user
        item.updated_at = int(time.time())
        item.updated_by = user and user.id or ""
        self.data[self._location][item.id] = item
        return True

    def search(self, domain: QueryDomain, limit=1000, offset=0) -> List[T]:
        items = []
        filter_function = self.parser.parse(domain)
        for item in list(self.data[self._location].values()):
            if filter_function(item):
                items.append(item)

        if offset is not None:
            items = items[offset:]

        if limit is not None:
            items = items[:min(limit, self.max_items)]

        return items

    def remove(self, item: T) -> bool:
        if item.id not in self.data[self._location]:
            return False
        del self.data[self._location][item.id]
        return True

    def load(self, data: Dict[str, Dict[str, T]]) -> None:
        self.data = data

    @property
    def _location(self) -> str:
        return self.tenant_provider.tenant.location('memory')
