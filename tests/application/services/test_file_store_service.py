from mediark.application.services import (
    FileStoreService, MemoryFileStoreService)
from mediark.application.utilities import (
    Tenant, StandardTenantProvider, StandardAuthProvider)


def test_file_store_service() -> None:
    methods = FileStoreService.__abstractmethods__  # type: ignore
    assert 'store' in methods


def test_memory_file_store_service_implementation() -> None:
    assert issubclass(MemoryFileStoreService, FileStoreService)


async def test_memory_file_store_service_store() -> None:
    file_id = 'ec892a1e-a05b-4152-b0e4-1be9b276005c'
    content = b'BASE64_ENCODED_CONTENT'
    contexts = [{
        'id': file_id,
        'content': content
    }]

    file_store_service = MemoryFileStoreService(
        StandardTenantProvider(),
        StandardAuthProvider())
    uri, *_ = await file_store_service.store(contexts)

    assert isinstance(uri, str)
    assert uri == file_id


async def test_memory_file_store_service_store_many() -> None:
    contexts = [
        {
            'id': 'ec892a1e-a05b-4152-b0e4-1be9b276005c',
            'content': b'BASE64_ENCODED_CONTENT'
        },
        {
            'id': '3054a584-2f8e-4a62-b480-0405b311a5aa',
            'content': b'BASE64_ENCODED_CONTENT'
        }
    ]

    file_store_service = MemoryFileStoreService(
        StandardTenantProvider(),
        StandardAuthProvider())

    uris = await file_store_service.store(contexts)

    assert len(uris) == len(contexts)
    assert uris[0] == contexts[0]['id']
    assert uris[1] == contexts[1]['id']
