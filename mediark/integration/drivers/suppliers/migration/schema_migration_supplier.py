from typing import List, Dict, Any
from pathlib import Path
from migrark import sql_migrate
from ..common import SchemaConnection
from .....application.general.suppliers import (
    MigrationSupplier, TenantSupplier)


class SchemaMigrationSupplier(MigrationSupplier):
    def __init__(self, zones: Dict[str, str],
                 tenant_supplier: TenantSupplier) -> None:
        self.zones = zones
        self.tenant_supplier = tenant_supplier
        self.template_schema = '__template__'
        self.migrations_path = str(
            (Path(__file__).parent.parent.parent / 'data' /
             'sql' / 'migrations').absolute())

    def migrate(self, tenant: str = '', version: str = '') -> None:
        domain = []
        if tenant:
            domain = [('slug', 'in', tenant.lower().split(','))]

        version = version or '999'

        tenants = self.tenant_supplier.search_tenants(domain)

        for zone, dsn in self.zones.items():
            schemas = [self.template_schema]
            for tenant_dict in tenants:
                tenant_zone: str = tenant_dict['zone'] or 'default'

                if tenant_zone == zone:
                    schemas.append(tenant_dict['slug'])

            connection = SchemaConnection(str(dsn))
            context = {'placeholder': '%s'}
            for schema in schemas:
                sql_migrate(connection, self.migrations_path,
                            schema, context=context,
                            target_version=version)
