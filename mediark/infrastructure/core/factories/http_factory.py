import json
from pathlib import Path
from ....application.repositories import ImageRepository, AudioRepository
from ...http import HttpMediarkReporter
from ..configuration import Config
from ....application.coordinators import SessionCoordinator
from ....application.utilities import TransactionManager, TenantProvider
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from .directory_factory import DirectoryFactory


class HttpFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def http_mediark_reporter(
        self, tenant_provider: TenantProvider,
        image_repository: ImageRepository,
        audio_repository: AudioRepository,
        transaction_manager: TransactionManager
    ) -> HttpMediarkReporter:
        return transaction_manager(HttpMediarkReporter)(
            self.config['domain'], tenant_provider,
            image_repository, audio_repository)
