from pathlib import Path
from ...application.utilities import (
    TenantProvider, StandardTenantProvider)
from ...infrastructure.data import (
    DirectoryFileStoreService)
from ..core import Config
from .memory_factory import MemoryFactory
from .http_factory import HttpFactory


class DirectoryFactory(HttpFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def directory_file_store_service(
        self, tenant_provider: TenantProvider
    ) -> DirectoryFileStoreService:
        return DirectoryFileStoreService(
            tenant_provider, self.config["data"])
