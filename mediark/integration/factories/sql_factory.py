from filtrark import SqlParser, SafeEval
from ...application.domain.common import (
    AuthProvider, TenantProvider, QueryParser,
    TransactionManager)
from ..core.suppliers.common.tenancy import (
    TenantSupplier, SchemaTenantSupplier)
from ...application.domain.repositories import MediaRepository
from ..core import Config
from ..core.suppliers.migration import (
    MigrationSupplier, SchemaMigrationSupplier)
from ..core.suppliers.common.connection import SchemaConnection
from ..core.data import (
    ConnectionManager, DefaultConnectionManager, SqlTransactionManager,
    SqlMediaRepository)
from .directory_factory import DirectoryFactory


class SqlFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def query_parser(self) -> QueryParser:
        return SqlParser(SafeEval(), jsonb_collection='data')

    def connection_manager(self) -> ConnectionManager:
        settings = []
        for zone, config in self.config['zones'].items():
            options = {'name': zone, 'dsn': config['dsn']}
            settings.append(options)
        return DefaultConnectionManager(settings)

    def transaction_manager(
        self, connection_manager: ConnectionManager,
        tenant_provider: TenantProvider
    ) -> TransactionManager:
        return SqlTransactionManager(connection_manager, tenant_provider)

    def media_repository(
        self, auth_provider: AuthProvider,
        connection_manager: ConnectionManager,
        sql_parser: QueryParser,
        tenant_provider: TenantProvider
    ) -> MediaRepository:
        return SqlMediaRepository(
            tenant_provider, auth_provider, connection_manager, sql_parser)

    def tenant_supplier(self) -> TenantSupplier:
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}
        connection = SchemaConnection(self.config['tenancy']['dsn'])
        return SchemaTenantSupplier(connection, zones)

    def migration_supplier(
            self, tenant_supplier: TenantSupplier) -> MigrationSupplier:
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}
        return SchemaMigrationSupplier(zones, tenant_supplier)
