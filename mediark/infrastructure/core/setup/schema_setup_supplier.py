from typing import Dict, Any
from pathlib import Path
from migrark import sql_migrate
from .memory_setup_supplier import MemorySetupSupplier


class SchemaSetupSupplier(MemorySetupSupplier):

    def __init__(self, zones: Dict[str, Any]) -> None:
        self.zones = zones

    def setup(self):
        target_version = '001'
        schema = '__template__'

        migrations_path = str(
            (Path(__file__).parent.parent / 'data' /
             'sql' / 'migrations').absolute())
        for zone, dsn in self.zones.items():
            database_uri = dsn
            sql_migrate(database_uri, migrations_path, schema,
                        target_version=target_version)
