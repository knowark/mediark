import os
from pathlib import Path
from filtrark import SqlParser, SafeEval
from ...application.domain.common import (
    AuthProvider, TenantProvider, QueryParser)
from ...application.general.connector import (
    Connector, Transactor)
from ...integration.core.data.sql import (
    SqlConnector, SqlTransactor)
from ...integration.core import Config
from ...application.general.suppliers import (
    TenantSupplier, PlanSupplier)
from ...integration.drivers import (
    SchemaTenantSupplier, SchemaMigrationSupplier, SchemaConnection,
    HttpEmailSupplier, SqlPlanSupplier)
from ...application.domain.services.repositories import (
    MediaRepository, EmailRepository)
from ..core.data import SqlMediaRepository, SqlEmailRepository
from .directory_factory import DirectoryFactory


class SqlFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def sql_parser(self) -> SqlParser:
        return SqlParser(SafeEval(), jsonb_collection='data')

    # Core

    def connector(self) -> Connector:
        settings = []
        for zone, config in self.config['zones'].items():
            options = {'name': zone, 'dsn': config['dsn']}
            settings.append(options)

        return SqlConnector(settings)

    def transactor(
        self, connection_manager: Connector,
        tenant_provider: TenantProvider
    ) -> Transactor:
        return SqlTransactor(connection_manager, tenant_provider)

    # Repositories
    def media_repository(
        self, tenant_provider: TenantProvider,
        auth_provider: AuthProvider,
        connection_manager: Connector,
        sql_parser: SqlParser
    ) -> MediaRepository:
        return SqlMediaRepository(
            tenant_provider, auth_provider, connection_manager, sql_parser)

    def email_repository(
        self, tenant_provider: TenantProvider,
        auth_provider: AuthProvider,
        connection_manager: Connector,
        sql_parser: SqlParser
    ) -> EmailRepository:
        return SqlEmailRepository(
            tenant_provider, auth_provider, connection_manager, sql_parser)

    def tenant_supplier(self) -> TenantSupplier:
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}
        connection = SchemaConnection(self.config['tenancy']['dsn'])
        return SchemaTenantSupplier(connection, zones)

    def email_supplier(self) -> HttpEmailSupplier:
        config = {**self.config.get('mail',{})}
        return HttpEmailSupplier(config)

    def migration_supplier(
            self, tenant_supplier: TenantSupplier
    ) -> SchemaMigrationSupplier:
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}
        return SchemaMigrationSupplier(zones, tenant_supplier)

    def plan_supplier(self, connector: Connector) -> PlanSupplier:
        return SqlPlanSupplier(connector)
