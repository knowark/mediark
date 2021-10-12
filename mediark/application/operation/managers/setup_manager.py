import time
import datetime
import asyncio
from typing import Dict, Union, Any
from ...general.suppliers import (
    PlanSupplier, MigrationSupplier, TenantSupplier)


class SetupManager:
    def __init__(
        self, plan_supplier: PlanSupplier,
        migration_supplier: MigrationSupplier
    ) -> None:
        self.plan_supplier = plan_supplier
        self.migration_supplier = migration_supplier

    async def prepare(self, entry: dict) -> dict:
        await self.plan_supplier.setup()
        self.migration_supplier.migrate()
        return {}
