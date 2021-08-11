from injectark import Factory
from pathlib import Path
from ...application.domain.common import (
    TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from ...application.domain.services.repositories import (
    RepositoryService,
    MediaRepository, MemoryMediaRepository)
from ...application.general.connector import (
    Connector, MemoryConnector, Transactor, MemoryTransactor)
from ...application.domain.services import (
    IdService, StandardIdService,
    CacheService, StandardCacheService,
    FileStoreService, MemoryFileStoreService)
from ...application.operation.managers import (
    SessionManager, MediaStorageManager)
from ...application.operation.informers import (
    FileInformer,
    StandardInformer, StandardFileInformer)
from ...application.general.suppliers import (
    TenantSupplier, MemoryTenantSupplier,
    MigrationSupplier, MemoryMigrationSupplier)
from ..core.common import Config


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.public = [
            'FileInformer', 'StandardInformer',
            'MediaStorageManager', 'SessionManager'
        ]

    # Providers

    def auth_provider(self) -> StandardAuthProvider:
        return StandardAuthProvider()

    def tenant_provider(self) -> StandardTenantProvider:
        return StandardTenantProvider()
    # General

    def connector(self) -> Connector:
        return MemoryConnector()

    def transactor(self) -> Transactor:
        return MemoryTransactor()

    # Suppliers

    def tenant_supplier(self) -> TenantSupplier:
        return MemoryTenantSupplier()

    def migration_supplier(self) -> MigrationSupplier:
        return MemoryMigrationSupplier()

    # Repositories

    def media_repository(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MediaRepository:
        return MemoryMediaRepository(
            locator=tenant_provider, editor=auth_provider)

    # Managers

    def session_manager(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider,
            tenant_supplier: TenantSupplier
    ) -> SessionManager:
        return SessionManager(
            tenant_provider, auth_provider, tenant_supplier)

    def media_storage_manager(self, media_repository: MediaRepository,
                              id_service: IdService,
                              file_store_service: FileStoreService,
                              transactor: Transactor
                              ) -> MediaStorageManager:
        return transactor(MediaStorageManager)(
            media_repository, id_service,
            file_store_service)

    # Services

    def id_service(self) -> IdService:
        return StandardIdService()

    def file_store_service(
            self, tenant_provider: TenantProvider
    ) -> FileStoreService:
        print("BASE FACTORY>>>>>"*50)

        return MemoryFileStoreService(tenant_provider)

    # Informers

    def standard_informer(
            self, transactor: Transactor, repository_service: RepositoryService
    ) -> StandardInformer:
        return transactor(StandardInformer)(repository_service)

    def file_informer(self, file_store_service: FileStoreService,
                      media_repository: MediaRepository,
                      transactor: Transactor
                      ) -> FileInformer:
        return transactor(StandardFileInformer)(
            file_store_service, media_repository)

    def repository_service(
        self, media_repository: MediaRepository) -> RepositoryService:

        repositories = locals()
        repositories.pop('self')
        return RepositoryService(repositories.values())
