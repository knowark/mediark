from abc import ABC, abstractmethod
from typing import List, Generic
from ..models import T
from ..utilities import QueryDomain


class Repository(ABC, Generic[T]):

    @abstractmethod
    def get(self, id: str) -> T:
        "Get method to be implemented."

    @abstractmethod
    def add(self, item: T) -> T:
        "Add method to be implemented."

    @abstractmethod
    def update(self, item: T) -> bool:
        "Update method to be implemented."

    @abstractmethod
    def search(self, domain: QueryDomain,
               limit: int = 0, offset: int = 0) -> List[T]:
        "Search items matching a query domain"

    @abstractmethod
    def remove(self, item: T) -> bool:
        "Remove method to be implemented."
