import types
from abc import ABC, abstractmethod
from typing import Callable


class TransactionManager(ABC):
    """Transaction manager."""

    @abstractmethod
    def __call__(self, cls: Callable) -> Callable:
        "__call__ method to be implemented."


class MemoryTransactionManager(TransactionManager):

    def __call__(self, cls: Callable) -> Callable:
        return cls
