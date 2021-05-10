from pathlib import Path
from ..application.domain.repositories import (
    MediaRepository, MemoryMediaRepository)
from ..application.domain.common import (
    User, QueryParser, TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider, TransactionManager,
    MemoryTransactionManager)
from ..application.domain.services import (
    IdService, StandardIdService,
    CacheService, StandardCacheService,
    FileStoreService, MemoryFileStoreService)
from ..application.managers import (
    SessionManager, MediaStorageManager)
from ..application.informers import (
    FileInformer, MediarkInformer,
    StandardMediarkInformer, StandardFileInformer)
from ..core import Config
from ..core.suppliers.common.tenancy import (
    TenantSupplier, MemoryTenantSupplier)
from ..core.suppliers.migration import (
    MigrationSupplier, MemoryMigrationSupplier)
from injectark import Factory


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def query_parser(self) -> QueryParser:
        return QueryParser()

    # Providers

    def tenant_provider(self) -> TenantProvider:
        return StandardTenantProvider()

    def auth_provider(self) -> AuthProvider:
        return StandardAuthProvider()

    # Suppliers

    def tenant_supplier(self) -> TenantSupplier:
        return MemoryTenantSupplier()

    def migration_supplier(self) -> MigrationSupplier:
        return MemoryMigrationSupplier()

    # Repositories

    def media_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MediaRepository:
        return MemoryMediaRepository(
            query_parser, tenant_provider, auth_provider)

    # Managers

    def transaction_manager(self) -> TransactionManager:
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

    # Services

    def id_service(self) -> IdService:
        return StandardIdService()

    def file_store_service(
            self, tenant_provider: TenantProvider
    ) -> FileStoreService:
        return MemoryFileStoreService(tenant_provider)

    # Informers

    def mediark_informer(self,
                         media_repository: MediaRepository,
                         transaction_manager: TransactionManager
                         ) -> MediarkInformer:
        return transaction_manager(
            StandardMediarkInformer)(media_repository)

    def file_informer(self, file_store_service: FileStoreService,
                      media_repository: MediaRepository,
                      transaction_manager: TransactionManager
                      ) -> FileInformer:
        return transaction_manager(StandardFileInformer)(
            file_store_service, media_repository)
