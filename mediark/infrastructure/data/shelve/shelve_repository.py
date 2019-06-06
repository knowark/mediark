import shelve
from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar, Optional, Generic, Union
from ....application.repositories import Repository
from ....application.utilities import ExpressionParser, T, QueryDomain
# from ....application.repositories import T, QueryDomain


class ShelveRepository(Repository, Generic[T]):
    def __init__(self,  parser: ExpressionParser, filename: str) -> None:
        self.filename = filename
        self.parser = parser

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
