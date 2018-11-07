from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar, Optional, Generic, Union
from .repository import Repository
from .expression_parser import ExpressionParser
from .types import T, QueryDomain


class MemoryRepository(Repository, Generic[T]):
    def __init__(self,  parser: ExpressionParser) -> None:
        self.items = {}  # type: Dict[str, T]
        self.parser = parser

    def get(self, id: str) -> Optional[T]:
        return self.items.get(id)

    def add(self, item: T) -> bool:
        id = getattr(item, 'id')
        self.items[id] = item
        return True

    def search(self, domain: QueryDomain, limit=0, offset=0) -> List[T]:
        items = []
        limit = int(limit) if limit > 0 else 100
        offset = int(offset) if offset > 0 else 0
        filter_function = self.parser.parse(domain)
        for item in list(self.items.values()):
            if filter_function(item):
                items.append(item)

        items = items[:limit]
        items = items[offset:]

        return items

    def remove(self, item: T) -> bool:
        id = getattr(item, 'id')
        if id not in self.items:
            return False
        del self.items[id]
        return True

    def load(self, items: Dict[str, T]) -> None:
        self.items = items
