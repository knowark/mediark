import inspect
import asyncio
import logging
from typing import Dict, List, Callable, Any
from contextvars import ContextVar
from asyncpg import Connection, create_pool
from asyncpg.pool import Pool
from ......application.domain.common import TenantProvider
from ......application.general.connector import (
    Connector, Transactor)


connections_var = ContextVar('connections', default=None)


class SqlConnector(Connector):
    def __init__(self, settings: List[Dict[str, Any]],
                 default: str = "") -> None:
        self.settings = settings
        self.pools: Dict[str, Pool] = {}
        self.default = default or self.settings[0]['name']
        self.logger = logging.getLogger(__name__)

    async def get(self, pool: str = "") -> Connection:
        connection: Connection = connections_var.get(None)

        if connection is None:
            if not self.pools:
                await self._setup()
            pool = pool or self.default
            try:
                self.logger.info(self.pools[pool].get_size())
                connection = await self.pools[pool].acquire()
            except Exception:
                self.logger.exception("Failed acquire pools.")
                await self._setup()
                connection = await self.pools[self.default].acquire()
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


class SqlTransactor(Transactor):
    def __init__(self, connector: Connector,
                 tenant_provider: TenantProvider) -> None:
        self.connector = connector
        self.tenant_provider = tenant_provider

    def __call__(self, cls):
        decorate_method = self._decorate_method
        transactionless = self.transactionless(cls)

        class TransactionClass(cls):
            def __getattribute__(self, name):
                method = cls.__getattribute__(self, name)
                if (inspect.iscoroutinefunction(method)
                        and not name.startswith('_')
                        and name not in transactionless):
                    return decorate_method(method)

                return method

        return TransactionClass

    def _decorate_method(self, method: Callable):
        connector = self.connector
        tenant_provider = self.tenant_provider

        async def transaction_method(*args, **kwargs):
            tenant = self.tenant_provider.tenant
            connection = await connector.get(tenant.zone)
            try:
                transaction = connection.transaction()
                await transaction.start()
                result = await method(*args, **kwargs)
                await transaction.commit()
            except Exception:
                await transaction.rollback()
                raise
            finally:
                await connector.put(connection, tenant.zone)

            return result

        return transaction_method
