from pathlib import Path
from ...application.utilities import (
    TenantProvider, StandardTenantProvider)
from ...infrastructure.data import (
    SwiftAuthSupplier, SwiftFileStoreService,
    SwiftImageFileStoreService, SwiftAudioFileStoreService)
from ..core import Config, HttpClientSupplier
from .memory_factory import MemoryFactory
from .directory_factory import DirectoryFactory
from .sql_factory import SqlFactory


class CloudFactory(SqlFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def swift_auth_supplier(
            self, client: HttpClientSupplier) -> SwiftAuthSupplier:
        auth_url = self.config['data']['cloud']['swift']['auth_url']
        username = self.config['data']['cloud']['swift']['username']
        password = self.config['data']['cloud']['swift']['password']
        return SwiftAuthSupplier(client, auth_url, username, password)

    def swift_image_file_store_service(
        self, tenant_provider: TenantProvider
    ) -> SwiftImageFileStoreService:
        return SwiftImageFileStoreService(
            tenant_provider, self.config["data"], None, "images")

    def swift_audio_file_store_service(
        self, tenant_provider: TenantProvider
    ) -> SwiftAudioFileStoreService:
        return SwiftAudioFileStoreService(
            tenant_provider, self.config["data"], None, "audios")

    def swift_file_store_service(
        self, tenant_provider: TenantProvider,
        auth_supplier: SwiftAuthSupplier,
        client: HttpClientSupplier
    ) -> SwiftFileStoreService:
        return SwiftFileStoreService(
            tenant_provider, auth_supplier, client, self.config["data"])
