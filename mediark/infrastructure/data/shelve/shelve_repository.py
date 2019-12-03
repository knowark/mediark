import shelve
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, TypeVar, Optional, Generic, Union
from ....application.repositories import Repository
from ....application.utilities import (
    QueryParser, T, QueryDomain, TenantProvider)


class ShelveRepository(Repository, Generic[T]):
    def __init__(
            self,  parser: QueryParser, tenant_service: TenantProvider,
            data_config: dict, data_type: str
    ) -> None:
        filename = Path("{0}/{1}/{2}/{3}".format(
            data_config["dir_path"],
            tenant_service.tenant.slug,
            data_config["shelve"]["dir_path"],
            data_config["shelve"][data_type]["database"]))

        filename.parent.mkdir(parents=True, exist_ok=True)

        self.filename = str(filename)
        self.parser = parser

        shelve.open(self.filename).close()

    def get(self, id: str) -> Optional[T]:
        with shelve.open(self.filename, 'r') as items:
            return items.get(id)

    def add(self, item: T) -> bool:
        id = getattr(item, 'id')
        with shelve.open(self.filename) as items:
            items[id] = item
        return True

    def search(self, domain: QueryDomain, limit=0, offset=0) -> List[T]:
        items = []
        limit = int(limit) if limit > 0 else 100
        offset = int(offset) if offset > 0 else 0
        filter_function = self.parser.parse(domain)
        with shelve.open(self.filename, 'r') as shelve_items:
            for item in list(shelve_items.values()):
                if filter_function(item):
                    items.append(item)

        items = items[:limit]
        items = items[offset:]

        return items

    def remove(self, item: T) -> bool:
        id = getattr(item, 'id')
        with shelve.open(self.filename) as items:
            if id not in items:
                return False
            del items[id]
        return True

    def load(self, items: Dict[str, T]) -> None:
        with shelve.open(self.filename) as db:
            db.update(items)

    def update(self, item: T) -> bool:
        """Not implemented"""
