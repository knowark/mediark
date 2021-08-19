import time
import datetime
import asyncio
from typing import Dict, Union, Any
from ...general.suppliers import (
     MigrationSupplier, TenantSupplier)


class SetupManager:
    def __init__(
        self, migration_supplier: MigrationSupplier
    ) -> None:
        self.migration_supplier = migration_supplier

    async def prepare(self, entry: dict) -> dict:
        self.migration_supplier.migrate()
        return {}

