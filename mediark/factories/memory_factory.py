from pathlib import Path
from ..application.domain.repositories import (
    MediaRepository, MemoryMediaRepository)
from ..application.domain.common import (
    User, QueryParser, TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider, TransactionManager,
    MemoryTransactionManager)
from ..application.domain.services import (
    IdService, StandardIdService,
    FileStoreService, MemoryFileStoreService)
from ..application.managers import (
    SessionManager, MediaStorageManager)
from ..application.informers import (
    StandardMediarkInformer, StandardFileInformer)
from ..core import Config, MemoryMigrationSupplier
from ..core.suppliers.common.tenancy import MemoryTenantSupplier
from injectark import Factory


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def query_parser(self) -> QueryParser:
        return QueryParser()

    # Providers

    def standard_tenant_provider(self) -> StandardTenantProvider:
        return StandardTenantProvider()

    def standard_auth_provider(self) -> StandardAuthProvider:
        return StandardAuthProvider()

    # Suppliers

    def memory_tenant_supplier(self) -> MemoryTenantSupplier:
        return MemoryTenantSupplier()

    def memory_migration_supplier(self) -> MemoryMigrationSupplier:
        return MemoryMigrationSupplier()

    # Repositories

    def memory_media_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MemoryMediaRepository:
        return MemoryMediaRepository(
            query_parser, tenant_provider, auth_provider)

    # Managers

    def memory_transaction_manager(self) -> MemoryTransactionManager:
        return MemoryTransactionManager()

    def session_manager(self, tenant_provider: TenantProvider,
                        auth_provider: AuthProvider,
                        transaction_manager: TransactionManager
                        ) -> SessionManager:
        return transaction_manager(SessionManager)(
            tenant_provider, auth_provider)

    def media_storage_manager(self, media_repository: MediaRepository,
                              id_service: IdService,
                              file_store_service: FileStoreService,
                              transaction_manager: TransactionManager
                              ) -> MediaStorageManager:
        return transaction_manager(MediaStorageManager)(
            media_repository, id_service,
            file_store_service)

    # Informers

    def standard_mediark_informer(self,
                                  media_repository: MediaRepository,
                                  transaction_manager: TransactionManager
                                  ) -> StandardMediarkInformer:
        return transaction_manager(
            StandardMediarkInformer)(media_repository)

    def standard_file_informer(self, file_store_service: FileStoreService
                               ) -> StandardFileInformer:
        return StandardFileInformer(file_store_service)

    # Services

    def standard_id_service(self) -> StandardIdService:
        return StandardIdService()

    def memory_file_store_service(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryFileStoreService:
        return MemoryFileStoreService(tenant_provider, auth_provider)
