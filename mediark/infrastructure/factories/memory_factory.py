from pathlib import Path
from .factory import Factory
from ...application.repositories import (
    MediaRepository, MemoryMediaRepository)
from ...application.utilities import (
    User, QueryParser, TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider, TransactionManager,
    MemoryTransactionManager)
from ...application.services import (
    IdService, StandardIdService,
    FileStoreService, MemoryFileStoreService)
from ...application.coordinators import (
    SessionCoordinator, MediaStorageCoordinator)
from ...application.reporters import (
    MediarkReporter, StandardMediarkReporter,
    FileReporter, StandardFileReporter)
from ..core import (
    Config, MemoryTenantSupplier, MemorySetupSupplier)


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def query_parser(self) -> QueryParser:
        return QueryParser()

    def memory_tenant_supplier(self) -> MemoryTenantSupplier:
        return MemoryTenantSupplier()

    def memory_setup_supplier(self) -> MemorySetupSupplier:
        return MemorySetupSupplier()

    def memory_transaction_manager(self) -> MemoryTransactionManager:
        return MemoryTransactionManager()

    def standard_tenant_provider(self) -> StandardTenantProvider:
        return StandardTenantProvider()

    def standard_auth_provider(self) -> StandardAuthProvider:
        return StandardAuthProvider(User(id="1", name="John Doe"))

    # Repositories

    def memory_media_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MemoryMediaRepository:
        return MemoryMediaRepository(
            query_parser, tenant_provider, auth_provider)

    # Services

    def standard_id_service(self) -> StandardIdService:
        return StandardIdService()

    def memory_file_store_service(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryFileStoreService:
        return MemoryFileStoreService(tenant_provider, auth_provider)

    # Coordinators

    def session_coordinator(self, tenant_provider: TenantProvider,
                            auth_provider: AuthProvider,
                            transaction_manager: TransactionManager
                            ) -> SessionCoordinator:
        return transaction_manager(SessionCoordinator)(
            tenant_provider, auth_provider)

    def media_storage_coordinator(self, media_repository: MediaRepository,
                                  id_service: IdService,
                                  file_store_service: FileStoreService,
                                  transaction_manager: TransactionManager
                                  ) -> MediaStorageCoordinator:
        return transaction_manager(MediaStorageCoordinator)(
            media_repository, id_service,
            file_store_service)

    # Reporters

    def standard_mediark_reporter(self,
                                  media_repository: MediaRepository,
                                  transaction_manager: TransactionManager
                                  ) -> StandardMediarkReporter:
        return transaction_manager(
            StandardMediarkReporter)(media_repository)

    def standard_file_reporter(self, file_store_service: FileStoreService
                               ) -> StandardFileReporter:
        return StandardFileReporter(file_store_service)
