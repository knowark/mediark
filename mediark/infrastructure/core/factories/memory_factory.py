from pathlib import Path
from .factory import Factory
from ..configuration import Config
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from ....application.repositories import (
    ImageRepository, MemoryImageRepository,
    AudioRepository, MemoryAudioRepository)
from ....application.utilities import (
    User, QueryParser, TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from ....application.services import (
    IdService, StandardIdService,
    FileStoreService, MemoryFileStoreService,
    ImageFileStoreService, MemoryImageFileStoreService,
    AudioFileStoreService, MemoryAudioFileStoreService)
from ...core import JsonTenantSupplier
from ....application.coordinators import (
    SessionCoordinator, ImageStorageCoordinator, AudioStorageCoordinator)
from ....application.reporters import MediarkReporter, StandardMediarkReporter
from ...web.helpers import DirectoryLoadSupplier


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def query_parser(self) -> QueryParser:
        return QueryParser()

    def memory_tenant_supplier(self) -> MemoryTenantSupplier:
        return MemoryTenantSupplier()

    def standard_tenant_provider(self) -> StandardTenantProvider:
        return StandardTenantProvider()

    def standard_auth_provider(self) -> StandardAuthProvider:
        return StandardAuthProvider(User(id="1", name="John Doe"))

    def directory_load_supplier(self) -> DirectoryLoadSupplier:
        return DirectoryLoadSupplier(
            data_path=self.config['data']['dir_path'],
            media_dir=self.config['data']['media']['dir_path'])

    # Repositories

    def memory_image_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            standard_auth_provider: AuthProvider) -> MemoryImageRepository:
        return MemoryImageRepository(
            query_parser, tenant_provider, standard_auth_provider)

    def memory_audio_repository(
            self, query_parser: QueryParser, tenant_provider: TenantProvider,
            standard_auth_provider: AuthProvider) -> MemoryAudioRepository:
        return MemoryAudioRepository(
            query_parser, tenant_provider, standard_auth_provider)

    # Services

    def standard_id_service(self) -> StandardIdService:
        return StandardIdService()

    def memory_image_file_store_service(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryImageFileStoreService:
        return MemoryImageFileStoreService(tenant_provider, auth_provider)

    def memory_audio_file_store_service(
        self, tenant_provider: TenantProvider,
        auth_provider: AuthProvider
    ) -> MemoryAudioFileStoreService:
        return MemoryAudioFileStoreService(tenant_provider, auth_provider)

    # Coordinators

    def session_coordinator(self, tenant_provider: TenantProvider,
                            auth_provider: AuthProvider
                            ) -> SessionCoordinator:
        return SessionCoordinator(tenant_provider, auth_provider)

    def image_storage_coordinator(self, image_repository: ImageRepository,
                                  id_service: IdService,
                                  file_store_service: ImageFileStoreService
                                  ) -> ImageStorageCoordinator:
        return ImageStorageCoordinator(image_repository, id_service,
                                       file_store_service)

    def audio_storage_coordinator(self, audio_repository: AudioRepository,
                                  id_service: IdService,
                                  file_store_service: AudioFileStoreService
                                  ) -> AudioStorageCoordinator:
        return AudioStorageCoordinator(audio_repository, id_service,
                                       file_store_service)

    # Reporters

    def memory_mediark_reporter(self, image_repository: ImageRepository,
                                audio_repository: AudioRepository
                                ) -> StandardMediarkReporter:
        return StandardMediarkReporter(image_repository, audio_repository)
