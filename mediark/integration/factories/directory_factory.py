from pathlib import Path
from ...application.domain.common import TenantProvider
from ...application.domain.services import FileStoreService
from ..core.suppliers import (
    DirectoryFileStoreService)
from ..core.common import Config
from .http_factory import HttpFactory


class DirectoryFactory(HttpFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def file_store_service(
        self, tenant_provider: TenantProvider
    ) -> FileStoreService:
        print("FACTORY>>>>"*50)
        print(self.config)
        return DirectoryFileStoreService(
            tenant_provider, self.config)
