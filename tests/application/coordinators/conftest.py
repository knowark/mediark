from pytest import fixture
from unittest import mock
from mediark.application.utilities import (
    QueryParser, Tenant, StandardTenantProvider,
    User,  StandardAuthProvider)
from mediark.application.services import (
    StandardIdService, MemoryFileStoreService)
from mediark.application.repositories import (
    MemoryAudioRepository, MemoryImageRepository)
from mediark.application.coordinators import (
    ImageStorageCoordinator, AudioStorageCoordinator)
from mediark.application.coordinators import SessionCoordinator


@fixture
def query_parser():
    return QueryParser()


@fixture
def tenant_provider():
    return StandardTenantProvider(Tenant(name="Default"))


@fixture
def auth_provider():
    return StandardAuthProvider(User(id="1", name="John Doe"))


@fixture
def standard_id_service():
    return StandardIdService()


@fixture
def file_store_service(tenant_provider, auth_provider):
    return MemoryFileStoreService(tenant_provider, auth_provider)


# Repositories

@fixture
def audio_repository(query_parser, tenant_provider):
    return MemoryAudioRepository(query_parser, tenant_provider)


@fixture
def image_repository(query_parser, tenant_provider):
    return MemoryImageRepository(query_parser, tenant_provider)


# Coordinators


@fixture
def audio_storage_coordinator(
        audio_repository, standard_id_service, file_store_service):
    return AudioStorageCoordinator(
        audio_repository, standard_id_service, file_store_service)


@fixture
def image_storage_coordinator(
        image_repository, standard_id_service, file_store_service):
    return ImageStorageCoordinator(
        image_repository, standard_id_service, file_store_service)


@fixture
def session_coordinator(tenant_provider, auth_provider):
    return SessionCoordinator(tenant_provider, auth_provider)
