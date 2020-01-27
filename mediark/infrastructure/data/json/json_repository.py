import os
import time
from pathlib import Path
from json import load, dump
from uuid import uuid4
from typing import Dict, List, Any, Type, Callable, Generic, Union
from ....application.models import T
from ....application.utilities import (
    TenantProvider, AuthProvider, QueryDomain,
    QueryParser, EntityNotFoundError)
from ....application.repositories import Repository


class JsonRepository(Repository, Generic[T]):
    def __init__(self, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 collection: str, item_class: Callable[..., T]) -> None:
        self.parser = parser
        self.tenant_provider = tenant_provider
        self.auth_provider = auth_provider
        self.collection = collection
        self.item_class: Callable[..., T] = item_class
        self.max_items = 1000

    async def get(self, id: str) -> T:
        with self._file_path.open() as f:
            data = load(f)
            items = data.get(self.collection, {})
            item_dict = items.get(id)
            if not item_dict:
                raise EntityNotFoundError(
                    f"The entity with id {id} was not found.")
            return self.item_class(**item_dict)

    async def add(self, item: Union[T, List[T]]) -> List[T]:
        data: Dict[str, Any] = {}
        with self._file_path.open() as f:
            data = load(f)
        user = self.auth_provider.user
        items = item if isinstance(item, list) else [item]
        for item in items:
            item.id = item.id or str(uuid4())
            item.created_at = int(time.time())
            item.created_by = user and user.id or ""
            item.updated_at = item.created_at
            item.updated_by = item.created_by
            data[self.collection].update({item.id: vars(item)})
            with self._file_path.open('w') as f:
                dump(data, f, indent=2)
        return items

    async def update(self, item: Union[T, List[T]]) -> bool:
        items = item if isinstance(item, list) else [item]
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection)
        for item in items:
            if item.id not in items_dict:
                return False

            user = self.auth_provider.user
            item.updated_at = int(time.time())
            item.updated_by = user and user.id or ""

            items_dict[item.id] = vars(item)

            with self._file_path.open('w') as f:
                dump(data, f, indent=2)
        return True

    async def count(self, domain: QueryDomain = None) -> int:
        count = 0
        domain = domain or []
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection, {})

        filter_function = self.parser.parse(domain)
        for item_dict in items_dict.values():

            if filter_function(self.item_class(**item_dict)):
                count += 1

        return count

    async def search(
            self, domain: QueryDomain, limit=1000, offset=0) -> List[T]:
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection, {})

        items = []
        filter_function = self.parser.parse(domain)
        for item_dict in items_dict.values():
            item = self.item_class(**item_dict)

            if filter_function(item):
                items.append(item)

        if offset is not None:
            items = items[offset:]

        if limit is not None:
            items = items[:min(limit, self.max_items)]

        return items

    async def remove(self, item: Union[T, List[T]]) -> bool:
        items = item if isinstance(item, list) else [item]
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection)

        for item in items:
            if item.id not in items_dict:
                return False

            del items_dict[item.id]

            with self._file_path.open('w') as f:
                dump(data, f, indent=2)
        return True

    @property
    def _file_path(self) -> Path:
        location = self.tenant_provider.tenant.location('directory')
        slug = self.tenant_provider.tenant.slug
        return Path(location) / slug / "json" / f"{ self.collection}.json"
