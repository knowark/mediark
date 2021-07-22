from functools import partial
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from contextvars import ContextVar
from asyncpg import Connection, create_pool
from asyncpg.pool import Pool


class ConnectionManager(ABC):
    @abstractmethod
    async def get(self, pool: str = "") -> Connection:
        """Get a database connection."""

    @abstractmethod
    async def put(self, connection: Connection, pool: str = "") -> None:
        """Put a database connection back in its pool."""


connections_var = ContextVar('connections', default=None)


class DefaultConnectionManager(ConnectionManager):
    def __init__(self, settings: List[Dict[str, Any]],
                 default: str = "") -> None:
        self.settings = settings
        self.pools: Dict[str, Pool] = {}
        self.default = default or self.settings[0]['name']

    async def get(self, pool: str = "") -> Connection:
        connection: Connection = connections_var.get(None)

        if connection is None:
            if self.pools == {}:
                await self._setup()
            pool = pool or self.default
            connection = await self.pools[pool].acquire()
            connections_var.set(connection)

        return connection

    async def put(self, connection: Connection, pool: str = ""):
        connections_var.set(None)
        pool = pool or self.default
        await self.pools[pool].release(connection)

    async def _setup(self):
        self.pools = self.pools or {}
        for settings in self.settings:
            options = dict(settings)
            pool_name = options.pop('name')
            self.pools[pool_name] = await create_pool(**options)
