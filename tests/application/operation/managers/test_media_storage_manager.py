from pytest import raises, fixture
from mediark.application.operation.managers import MediaStorageManager
from mediark.application.domain.services.repositories import (
    MemoryMediaRepository)
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
def media_repository(parser, tenant_provider, auth_provider):
    return MemoryMediaRepository(parser, tenant_provider, auth_provider)

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
def file_store_service(tenant_provider):
    return MemoryFileStoreService(tenant_provider)


def test_storage_manager_instantiation(media_storage_manager):
    assert media_storage_manager is not None


async def test_storage_manager_submit_many(media_storage_manager):
    media_records = {
        "meta":{},
        "data": [
        {'media': {
            'name': 'example.png',
            'type': 'image/png',
            'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        }},
        {'media': {
            'name': 'photo.png',
            'type': 'image/png',
            'reference': '546bc220-dec1-415d-9f25-53be060bfc7e',
        }}
    ]}

    await media_storage_manager.submit(media_records)

    assert len(
        media_storage_manager.media_repository.data['default']) == 2


async def test_storage_manager_submit_file(media_storage_manager):
    class MockReader:
        data = b'FILE_STREAM_BINARY_DATA'

        async def read(self, size: int) -> bytes:
            return self.data

    stream = MockReader()

    submission_dict = {
        "meta":{},
        "data":[{
            'media': {
                'name': 'photo.png',
                'type': 'image/png',
                'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
            },
            'stream': stream
        }]
    }

    await media_storage_manager.submit(submission_dict)

    assert len(
        media_storage_manager.media_repository.data) == 1


async def test_storage_manager_delete(media_storage_manager):
    class MockReader:
        data = b'FILE_STREAM_BINARY_DATA'

        async def read(self, size: int) -> bytes:
            return self.data

    stream = MockReader()

    media_records = {
        "meta":{},
        "data": [{
            'media': {
                'id': 'ef4581b6-2136-4fb8-9be2-3a4fc1c83a02',
                'name': 'sample.jpg',
                'type': 'image/jpeg',
                'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
            },
            'stream': stream
        }]
    }

    await media_storage_manager.submit(media_records)

    assert len(
        media_storage_manager.media_repository.data['default']) == 1
    assert len(
        media_storage_manager.file_store_service.files['default']) == 1

    deletion_records = {
        "meta":{},
        "data": [{'id': 'ef4581b6-2136-4fb8-9be2-3a4fc1c83a02'
                  }]
        }
    await media_storage_manager.delete(deletion_records)

    assert len(
        media_storage_manager.media_repository.data['default']) == 0
    assert len(
        media_storage_manager.file_store_service.files['default']) == 0
