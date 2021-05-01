from pytest import fixture
from mediark.application.domain.services import (
    FileStoreService, MemoryFileStoreService)
from mediark.application.domain.common import (
    Tenant, User, StandardTenantProvider, StandardAuthProvider)


def test_file_store_service() -> None:
    methods = FileStoreService.__abstractmethods__  # type: ignore
    assert 'load' in methods
    assert 'submit' in methods


def test_memory_file_store_service_implementation() -> None:
    assert issubclass(MemoryFileStoreService, FileStoreService)


@fixture
def file_store_service():
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="Default"))

    file_store_service = MemoryFileStoreService(tenant_provider)

    return file_store_service


async def test_memory_file_store_service_load(file_store_service) -> None:
    uri = 'ec892a1e-a05b-4152-b0e4-1be9b276005c'
    file_store_service.files = {
        'default': {
            uri: b'IMAGE_BINARY_DATA'
        }
    }

    class MockWriter:
        data = None

        async def write(self, data: bytes) -> None:
            self.data = data

    mock_writer = MockWriter()

    await file_store_service.load(uri, mock_writer)

    assert mock_writer.data == b'IMAGE_BINARY_DATA'


async def test_memory_file_store_service_submit(file_store_service) -> None:
    uri = 'ec892a1e-a05b-4152-b0e4-1be9b276005c'
    chunk_1 = b'FIRST_BINARY_CHUNK\n'
    chunk_2 = b'SECOND_BINARY_CHUNK\n'
    chunk_3 = b'THIRD_BINARY_CHUNK'

    class MockReader:
        data = None

        async def read(self, size: int) -> None:
            chunk_1 = b'FIRST_BINARY_CHUNK\n'
            chunk_2 = b'SECOND_BINARY_CHUNK\n'
            chunk_3 = b'THIRD_BINARY_CHUNK'
            return chunk_1 + chunk_2 + chunk_3

    mock_reader = MockReader()

    contexts = [{
        'id': uri,
        'stream': mock_reader
    }]

    uris = await file_store_service.submit(contexts)

    assert uris == [uri]
    assert file_store_service.files['default'][uri] == (
        b'FIRST_BINARY_CHUNK\n'
        b'SECOND_BINARY_CHUNK\n'
        b'THIRD_BINARY_CHUNK'
    )


async def test_memory_file_store_service_delete(file_store_service) -> None:
    uri = 'ec892a1e-a05b-4152-b0e4-1be9b276005c'
    file_store_service.files = {
        'default': {
            uri: b'IMAGE_BINARY_DATA'
        }
    }

    assert len(file_store_service.files['default']) == 1

    await file_store_service.delete(uri)

    assert len(file_store_service.files['default']) == 0
