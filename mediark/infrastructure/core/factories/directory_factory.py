from pathlib import Path
from ....application.utilities import (
    TenantProvider, StandardTenantProvider)
from ....infrastructure.data import (
    DirectoryImageFileStoreService, DirectoryAudioFileStoreService)
from ..configuration import Config
from .memory_factory import MemoryFactory


class DirectoryFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def directory_image_file_store_service(
        self, tenant_provider: TenantProvider
    ) -> DirectoryImageFileStoreService:
        return DirectoryImageFileStoreService(
            tenant_provider, self.config["data"], "images")

    def directory_audio_file_store_service(
        self, tenant_provider: TenantProvider
    ) -> DirectoryAudioFileStoreService:
        return DirectoryAudioFileStoreService(
            tenant_provider, self.config["data"], "audios")
