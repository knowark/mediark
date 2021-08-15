from typing import (
    List, Tuple, Mapping, Protocol, Callable, Any, AsyncContextManager)
from contextlib import AsyncExitStack
from .connector import Connector, Connection, Transactor


class MemoryConnection:
    def __init__(self, fetch_results = [], execute_results = []) -> None:
        self.fetch_arguments: List[Tuple] = []
        self.fetch_results = fetch_results
        self.execute_arguments: List[Tuple] = []
        self.execute_results = execute_results

    async def fetch(self, query: str, *args, **kwargs) -> List[Mapping]:
        self.fetch_arguments.append((query, args, kwargs))
        return len(self.fetch_results) and self.fetch_results.pop(0) or []

    async def execute(self, query: str, *args, **kwargs) -> str:
        self.execute_arguments.append((query, args, kwargs))
        return len(self.execute_results) and self.execute_results.pop(0) or ''

    def transaction(self) -> AsyncContextManager:
        return AsyncExitStack()


class MemoryConnector(Connector):
    def __init__(self, connection = None) -> None:
        self.connection = connection or MemoryConnection()

    async def get(self, pool: str = "") -> Connection:
        return self.connection

    async def put(self, connection: Connection, pool: str = "") -> None:
        """Put a connection back in its pool."""


class MemoryTransactor(Transactor):
    def __call__(self, cls: Callable) -> Callable:
        return cls
