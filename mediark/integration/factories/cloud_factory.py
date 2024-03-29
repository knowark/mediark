from pathlib import Path
from ...application.domain.services import (
    FileStoreService)
from ...application.domain.common import (
    TenantProvider, StandardTenantProvider)
from ..core.suppliers import (
    SwiftAuthSupplier, SwiftFileStoreService)
from ...integration.drivers import (
    HttpEmailSupplier)
from ..core.common import Config
from ..core.http import HttpClientSupplier
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

    def file_store_service(
        self, tenant_provider: TenantProvider,
        auth_supplier: SwiftAuthSupplier,
        client: HttpClientSupplier
    ) -> FileStoreService:
        return SwiftFileStoreService(
            tenant_provider, auth_supplier, client, self.config)

    def email_supplier(self) -> HttpEmailSupplier:
        config = {**self.config.get('mail',{})}
        return HttpEmailSupplier(config)
