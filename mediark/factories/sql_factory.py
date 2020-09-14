import json
from pathlib import Path
from uuid import uuid4
from filtrark import SqlParser, SafeEval
from ...application.utilities import (
    AuthProvider, StandardAuthProvider, StandardTenantProvider,
    TenantProvider, User)
from ..config import Config
from ..core import (
    TenantSupplier, SchemaTenantSupplier, SchemaSetupSupplier)
from ..data import (
    ConnectionManager, DefaultConnectionManager, SqlTransactionManager,
    SqlRepository, SqlMediaRepository)
from .directory_factory import DirectoryFactory


class SqlFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def sql_query_parser(self) -> SqlParser:
        return SqlParser(SafeEval())

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

    def schema_tenant_supplier(self) -> SchemaTenantSupplier:
        catalog = self.config['tenancy']['dsn']
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}
        return SchemaTenantSupplier(catalog, zones)

    def sql_media_repository(
        self, auth_provider: AuthProvider,
        connection_manager: ConnectionManager,
        sql_parser: SqlParser,
        tenant_provider: TenantProvider
    ) -> SqlMediaRepository:
        return SqlMediaRepository(
            tenant_provider, auth_provider, connection_manager, sql_parser)

    def schema_setup_supplier(self) -> SchemaSetupSupplier:
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}
        return SchemaSetupSupplier(zones)
