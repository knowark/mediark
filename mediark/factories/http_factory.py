import json
from pathlib import Path
from ..application.domain.repositories import MediaRepository
from ..application.managers import SessionManager
from ..application.domain.common import TransactionManager, TenantProvider
from ..core import Config
from ..core.suppliers.common.tenancy import (
    TenantSupplier, MemoryTenantSupplier)
from ..core.client import HttpClientSupplier
from ..presenters.rest.helpers import HttpMediarkInformer
from .memory_factory import MemoryFactory


class HttpFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def http_mediark_informer(
        self, tenant_provider: TenantProvider,
        media_repository: MediaRepository,
        transaction_manager: TransactionManager
    ) -> HttpMediarkInformer:
        return transaction_manager(HttpMediarkInformer)(
            self.config['domain'], tenant_provider,
            media_repository)

    def http_client_supplier(self) -> HttpClientSupplier:
        return HttpClientSupplier()
