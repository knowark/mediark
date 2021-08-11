import json
from pathlib import Path
from ...application.domain.services.repositories import (
    RepositoryService, MediaRepository)
from ...application.operation.informers import StandardInformer
from ...application.general.connector import Transactor
from ...application.domain.common import TenantProvider
from ..core.common import Config
from ..core.http import HttpClientSupplier
from ...presentation.platform.rest.helpers import HttpMediarkInformer
from .base_factory import BaseFactory


class HttpFactory(BaseFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def standard_informer(
        self, tenant_provider: TenantProvider,
        repository_service: RepositoryService,
        transactor: Transactor
    ) -> StandardInformer:
        return transactor(HttpMediarkInformer)(
            self.config['domain'], tenant_provider, repository_service
        )

    # def mediark_informer(
        # self, tenant_provider: TenantProvider,
        # media_repository: MediaRepository,
        # transactor: Transactor
    # ) -> MediarkInformer:
        # return transactor(HttpMediarkInformer)(
            # self.config['domain'], tenant_provider,
            # media_repository)

    def http_client_supplier(self) -> HttpClientSupplier:
        return HttpClientSupplier()
