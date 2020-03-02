from pathlib import Path
from ..configuration import Config
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from .memory_factory import MemoryFactory


class CheckFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def check_tenant_supplier(self) -> MemoryTenantSupplier:
        tenant_supplier = MemoryTenantSupplier()
        tenant_supplier.create_tenant({
            'id': '001',
            'name': 'Default',
            'zone': 'default'
        })
        return tenant_supplier
