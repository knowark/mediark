import inspect
from typing import Callable
from asyncpg import Connection
from .....application.domain.common import TransactionManager, TenantProvider
from .connection_manager import ConnectionManager


class SqlTransactionManager(TransactionManager):

    def __init__(self, connection_manager: ConnectionManager,
                 tenant_provider: TenantProvider) -> None:
        self.connection_manager = connection_manager
        self.tenant_provider = tenant_provider

    def __call__(self, cls):
        decorate_method = self._decorate_method

        class TransactionClass(cls):
            def __getattribute__(self, name):
                method = cls.__getattribute__(self, name)

                if (inspect.iscoroutinefunction(method) and
                        not name.startswith('_')):
                    return decorate_method(method)

                return method

        return TransactionClass

    def _decorate_method(self, method: Callable):
        connection_manager = self.connection_manager
        tenant_provider = self.tenant_provider

        async def transaction_method(*args, **kwargs):
            tenant = self.tenant_provider.tenant
            try:
                connection = await connection_manager.get(tenant.zone)
                transaction = connection.transaction()
                await transaction.start()
                result = await method(*args, **kwargs)
                await transaction.commit()
            except Exception as error:
                await transaction.rollback()
                raise
            finally:
                await connection_manager.put(connection, tenant.zone)

            return result

        return transaction_method
