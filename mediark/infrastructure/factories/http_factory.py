import json
from pathlib import Path
from ...application.repositories import MediaRepository
from ...application.coordinators import SessionCoordinator
from ...application.utilities import TransactionManager, TenantProvider
from ..config import Config
from ..core import (
    TenantSupplier, MemoryTenantSupplier, HttpClientSupplier)
from ..web import HttpMediarkReporter
from .memory_factory import MemoryFactory


class HttpFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def http_mediark_reporter(
        self, tenant_provider: TenantProvider,
        media_repository: MediaRepository,
        transaction_manager: TransactionManager
    ) -> HttpMediarkReporter:
        return transaction_manager(HttpMediarkReporter)(
            self.config['domain'], tenant_provider,
            media_repository)

    def http_client_supplier(self) -> HttpClientSupplier:
        return HttpClientSupplier()
