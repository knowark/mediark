from mediark.application.services import (
    FileStoreService, MemoryFileStoreService)


def test_file_store_service() -> None:
    methods = FileStoreService.__abstractmethods__  # type: ignore
    assert 'store' in methods


def test_memory_file_store_service_implementation() -> None:
    assert issubclass(MemoryFileStoreService, FileStoreService)


def test_memory_file_store_service_store() -> None:
    locator = 'ec892a1e-a05b-4152-b0e4-1be9b276005c'
    content = 'BASE64_ENCODED_CONTENT'

    file_store_service = MemoryFileStoreService()
    uri = file_store_service.store(locator, content)

    assert isinstance(uri, str)
    assert uri == locator
