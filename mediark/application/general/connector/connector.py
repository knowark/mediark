from abc import ABC, abstractmethod
from typing import List, Type, Mapping, Protocol
from typing import Callable


class Connection(Protocol):
    async def fetch(self, query: str, *args, **kwargs) -> List[Mapping]:
        """Fetch the given query records"""

    async def execute(self, query: str, *args, **kwargs) -> str:
        """Executre the given query records"""


class Connector(ABC):
    @abstractmethod
    async def get(self, pool: str = "") -> Connection:
        """Get a connection."""

    @abstractmethod
    async def put(self, connection: Connection, pool: str = "") -> None:
        """Put a connection back in its pool."""


class Transactor(ABC):
    @staticmethod
    def transactionless(target: Type) -> List[str]:
        """Target classes may define a transactionless
        attribute to define the methods that should not
        run in a transaction.
        """
        return getattr(target, 'transactionless', [])

    @abstractmethod
    def __call__(self, target: Callable) -> Callable:
        "__call__ method to be implemented."
