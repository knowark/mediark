import json
from pathlib import Path
from uuid import uuid4
from filtrark import SqlParser, SafeEval
from migrark import sql_migrate
from ..configuration import Config
from mediark.infrastructure.data import (
    ConnectionManager, DefaultConnectionManager, SqlTransactionManager,
    SqlRepository, SqlAudioRepository, SqlImageRepository)
from ...core import TenantSupplier, SchemaTenantSupplier
from .http_factory import HttpFactory
from mediark.application.utilities import (
    AuthProvider, StandardAuthProvider, StandardTenantProvider, TenantProvider,
    User)


class SqlFactory(HttpFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._setup()

    def _setup(self):
        target_version = '001'
        schema = '__template__'

        migrations_path = str(
            (Path(__file__).parent.parent / 'data' /
             'sql' / 'migrations').absolute())
        for zone, config in self.config['zones'].items():
            database_uri = config['dsn']
            sql_migrate(database_uri, migrations_path, schema,
                        target_version=target_version)

    def sql_query_parser(self) -> SqlParser:
        return SqlParser(SafeEval())

    def sql_connection_manager(self) -> DefaultConnectionManager:
        settings = []
        for zone, config in self.config['zones'].items():
            pool_config = config['pool']
            pool_config['name'] = zone
            pool_config['dsn'] = config['dsn']
            settings.append(pool_config)

        return DefaultConnectionManager(settings)

    def sql_transaction_manager(
        self, connection_manager: ConnectionManager,
        tenant_provider: TenantProvider
    ) -> SqlTransactionManager:
        return SqlTransactionManager(connection_manager, tenant_provider)

    def schema_tenant_supplier(self) -> TenantSupplier:
        catalog = self.config['tenancy']['dsn']
        zones = {key: value['dsn'] for key, value in
                 self.config['zones'].items()}

        return SchemaTenantSupplier(catalog, zones)

    def sql_audio_repository(
        self, auth_provider: AuthProvider,
        connection_manager: ConnectionManager,
        sql_parser: SqlParser,
        tenant_provider: TenantProvider
    ) -> SqlAudioRepository:
        return SqlAudioRepository(
            tenant_provider, auth_provider, connection_manager, sql_parser)

    def sql_image_repository(
        self, auth_provider: AuthProvider,
        connection_manager: ConnectionManager,
        sql_parser: SqlParser,
        tenant_provider: TenantProvider
    ) -> SqlImageRepository:
        return SqlImageRepository(
            tenant_provider, auth_provider, connection_manager, sql_parser)
