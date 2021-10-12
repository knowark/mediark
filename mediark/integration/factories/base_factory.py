from injectark import Factory
from pathlib import Path
from ...application.domain.common import (
    TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from ...application.domain.services.repositories import (
    RepositoryService,
    MediaRepository, MemoryMediaRepository,
    EmailRepository, MemoryEmailRepository)
from ...application.general.connector import (
    Connector, MemoryConnector, Transactor, MemoryTransactor)
from ...application.domain.services import (
    IdService, StandardIdService,
    CacheService, StandardCacheService,
    FileStoreService, MemoryFileStoreService)
from ...application.operation.managers import (
    SessionManager, MediaStorageManager, EmailManager, SetupManager)
from ...application.operation.informers import (
    FileInformer,
    StandardInformer, StandardFileInformer)
from ...application.general.suppliers import (
    TenantSupplier, MemoryTenantSupplier,
    MigrationSupplier, MemoryMigrationSupplier,
    EmailSupplier, MemoryEmailSupplier,
    PlanSupplier, MemoryPlanSupplier)
from ..core.common import Config


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.public = [
            'FileInformer', 'StandardInformer', 'EmailManager',
            'MediaStorageManager', 'SessionManager', 'SetupManager'
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

    def email_supplier(self) -> EmailSupplier:
        return MemoryEmailSupplier()

    def plan_supplier(
        self, connector: Connector,
    ) -> PlanSupplier:
        return MemoryPlanSupplier()

    # Repositories

    def media_repository(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MediaRepository:
        return MemoryMediaRepository(
            locator=tenant_provider, editor=auth_provider)

    def email_repository(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> EmailRepository:
        return MemoryEmailRepository(
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

    def email_manager(self, transactor: Transactor,
                      email_supplier: EmailSupplier,
                      email_repository: EmailRepository,
                      plan_supplier: PlanSupplier,
                      tenant_provider: TenantProvider,
                      auth_provider: AuthProvider
                      ) -> EmailManager:
        config = {**self.config.get('mail',{})}
        return EmailManager(config, email_supplier, email_repository,
                            plan_supplier, tenant_provider, auth_provider)

    def setup_manager(
        self, plan_supplier: PlanSupplier,
        migration_supplier: MigrationSupplier
    ) -> SetupManager:
        return SetupManager(
            plan_supplier, migration_supplier)

    # Services

    def id_service(self) -> IdService:
        return StandardIdService()

    def file_store_service(
            self, tenant_provider: TenantProvider
    ) -> FileStoreService:

        return MemoryFileStoreService(tenant_provider)

    # Informers

    def standard_informer(
            self, transactor: Transactor,
            repository_service: RepositoryService
    ) -> StandardInformer:
        return transactor(StandardInformer)(repository_service)

    def file_informer(self, file_store_service: FileStoreService,
                      media_repository: MediaRepository,
                      transactor: Transactor
                      ) -> FileInformer:
        return transactor(StandardFileInformer)(
            file_store_service, media_repository)

    def repository_service(
        self, media_repository: MediaRepository,
        email_repository: EmailRepository) -> RepositoryService:

        repositories = locals()
        repositories.pop('self')
        return RepositoryService(repositories.values())
