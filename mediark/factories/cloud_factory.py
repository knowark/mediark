from pathlib import Path
from ..application.domain.common import (
    TenantProvider, StandardTenantProvider)
from ..core.suppliers import (
    SwiftAuthSupplier, SwiftFileStoreService)
from ..core import Config
from ..core.client import HttpClientSupplier
from .memory_factory import MemoryFactory
from .directory_factory import DirectoryFactory
from .sql_factory import SqlFactory


class CloudFactory(SqlFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def swift_auth_supplier(
            self, client: HttpClientSupplier) -> SwiftAuthSupplier:
        auth_url = self.config['cloud']['swift']['auth_url']
        username = self.config['cloud']['swift']['username']
        password = self.config['cloud']['swift']['password']
        return SwiftAuthSupplier(client, auth_url, username, password)

    def swift_file_store_service(
        self, tenant_provider: TenantProvider,
        auth_supplier: SwiftAuthSupplier,
        client: HttpClientSupplier
    ) -> SwiftFileStoreService:
        return SwiftFileStoreService(
            tenant_provider, auth_supplier, client, self.config)
