import json
from pathlib import Path
from ...application.domain.services.repositories import MediaRepository
from ...application.operation.informers import MediarkInformer
from ...application.domain.common import TransactionManager, TenantProvider
from ..core import Config
from ..core.http import HttpClientSupplier
from ...presentation.rest.helpers import HttpMediarkInformer
from .base_factory import BaseFactory


class HttpFactory(BaseFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def mediark_informer(
        self, tenant_provider: TenantProvider,
        media_repository: MediaRepository,
        transaction_manager: TransactionManager
    ) -> MediarkInformer:
        return transaction_manager(HttpMediarkInformer)(
            self.config['domain'], tenant_provider,
            media_repository)

    def http_client_supplier(self) -> HttpClientSupplier:
        return HttpClientSupplier()
