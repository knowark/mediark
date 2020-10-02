from filtrark import SqlParser, SafeEval
from ..application.domain.common import AuthProvider, TenantProvider
from ..core.suppliers.common.tenancy import (
    TenantSupplier, SchemaTenantSupplier)
from ..core import Config
from ..core.suppliers.migration import SchemaMigrationSupplier
from ..core.suppliers.common.connection import SchemaConnection
from ..core.data import (
    ConnectionManager, DefaultConnectionManager, SqlTransactionManager,
    SqlMediaRepository)
from .directory_factory import DirectoryFactory


class SqlFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def sql_query_parser(self) -> SqlParser:
        return SqlParser(SafeEval(), jsonb_collection='data')

    def sql_connection_manager(self) -> DefaultConnectionManager:
        settings = []
        for zone, config in self.config['zones'].items():
            options = {'name': zone, 'dsn': config['dsn']}
            settings.append(options)
        return DefaultConnectionManager(settings)

    def sql_transaction_manager(
        self, connection_manager: ConnectionManager,
        tenant_provider: TenantProvider
    ) -> SqlTransactionManager:
        return SqlTransactionManager(connection_manager, tenant_provider)

    def sql_media_repository(
        self, auth_provider: AuthProvider,
        connection_manager: ConnectionManager,
        sql_parser: SqlParser,
        tenant_provider: TenantProvider
    ) -> SqlMediaRepository:
        return SqlMediaRepository(
            tenant_provider, auth_provider, connection_manager, sql_parser)

    def schema_tenant_supplier(self) -> SchemaTenantSupplier:
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}
        connection = SchemaConnection(self.config['tenancy']['dsn'])
        return SchemaTenantSupplier(connection, zones)

    def schema_migration_supplier(
            self, tenant_supplier: TenantSupplier) -> SchemaMigrationSupplier:
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}
        return SchemaMigrationSupplier(zones, tenant_supplier)
