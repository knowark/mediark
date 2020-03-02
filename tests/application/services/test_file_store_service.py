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
    content = 'BASE64_ENCODED_CONTENT'

    file_store_service = MemoryFileStoreService(
        StandardTenantProvider(),
        StandardAuthProvider())
    uri = await file_store_service.store(file_id, content)

    assert isinstance(uri, str)
    assert uri == file_id
