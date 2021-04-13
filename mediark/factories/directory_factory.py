from pathlib import Path
from ..application.domain.common import TenantProvider
from ..application.domain.services import FileStoreService
from ..core.suppliers import (
    DirectoryFileStoreService)
from ..core import Config
from .http_factory import HttpFactory


class DirectoryFactory(HttpFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def file_store_service(
        self, tenant_provider: TenantProvider
    ) -> FileStoreService:
        return DirectoryFileStoreService(
            tenant_provider, self.config)
