
from pytest import raises, fixture
from mediark.application.managers import MediaStorageManager
from mediark.application.domain.repositories import MemoryMediaRepository
from mediark.application.domain.common import (
    QueryParser, Tenant, StandardTenantProvider,
    User,  StandardAuthProvider)
from mediark.application.domain.services import (
    StandardIdService, MemoryFileStoreService)


@fixture
def parser() -> QueryParser:
    return QueryParser()

# Provider


@fixture
def tenant_provider() -> StandardTenantProvider:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="default"))
    return tenant_provider


@fixture
def auth_provider() -> StandardAuthProvider:
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(id='001', name='johndoe'))
    return auth_provider

# Repositories


@fixture
def media_repository(tenant_provider, auth_provider):
    return MemoryMediaRepository(QueryParser, tenant_provider, auth_provider)

# Managers


@fixture
def media_storage_manager(
        media_repository, standard_id_service, file_store_service):
    return MediaStorageManager(
        media_repository, standard_id_service, file_store_service)

# Services


@fixture
def standard_id_service():
    return StandardIdService()


@fixture
def file_store_service(tenant_provider, auth_provider):
    return MemoryFileStoreService(tenant_provider, auth_provider)


def test_storage_manager_instantiation(media_storage_manager):
    assert media_storage_manager is not None


async def test_storage_manager_store_no_data(media_storage_manager):
    media_dict = [{
        'type': 'images',
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'extension': 'jpg'
    }]
    with raises(ValueError):
        await media_storage_manager.store(media_dict)


async def test_storage_manager_store_data(media_storage_manager):
    media_dict = [{
        'type': 'images',
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': 'QkFTRTY0X0RBVEE=',  # BASE64_DATA
        'extension': 'jpg'
    }]

    await media_storage_manager.store(media_dict)

    assert len(
        media_storage_manager.media_repository.data['default']) == 1


async def test_storage_manager_store_file(media_storage_manager):
    media_dict = [{
        'type': 'images',
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': ('"iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42'
                 'mNk+H+1noEIwDiqkL4KAUP4F0koL9m+AAAAAElFTkSuQmCC",'),
        'extension': 'png'
    }]

    await media_storage_manager.store(media_dict)

    assert len(
        media_storage_manager.media_repository.data) == 1


async def test_storage_manager_store_data_many(media_storage_manager):
    media_records = [
        {
            'type': 'images',
            'namespace': 'https://example.com',
            'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
            'data': 'QkFTRTY0X0RBVEE=',  # BASE64_DATA
            'extension': 'jpg'
        },
        {
            'type': 'images',
            'namespace': 'https://example.com',
            'reference': '546bc220-dec1-415d-9f25-53be060bfc7e',
            'data': 'T1RIRVJfQkFTRTY0X0RBVEE=',  # OTHER_BASE64_DATA
            'extension': 'jpg'
        }
    ]

    await media_storage_manager.store(media_records)

    assert len(
        media_storage_manager.media_repository.data['default']) == 2
