from pytest import fixture, raises
from mediark.application.domain.common import (
    QueryParser, Tenant, StandardTenantProvider, Tenant,
    AuthProvider, StandardAuthProvider, User, QueryDomain,
    MediaNotFoundError)
from mediark.application.domain.models import Media
from mediark.application.domain.services import (
    MemoryFileStoreService, StandardCacheService)
from mediark.application.domain.services.repositories import MemoryMediaRepository
from mediark.application.operation.informers import FileInformer, StandardFileInformer


@fixture
def media_repository():
    parser = QueryParser()
    auth_provider = StandardAuthProvider()
    tenant_service = StandardTenantProvider()
    media_repository = MemoryMediaRepository(
        parser, tenant_service, auth_provider)
    media_repository.load({
        'default': {
            '001': Media(
                id='001', reference='ABC',
                path='images/abcd1234.jpg',
                uri='data/abcd1234.jpg'),
            '002': Media(id='002', reference='XYZ')
        }
    })
    return media_repository


@fixture
def file_informer(media_repository):
    tenant_provider = StandardTenantProvider()
    file_store_service = MemoryFileStoreService(tenant_provider)
    return StandardFileInformer(
        file_store_service, media_repository)


def test_file_informer_instantiation(file_informer):
    assert isinstance(file_informer, FileInformer)


async def test_file_informer_load(file_informer):
    path = 'images/abcd1234.jpg'

    class MockWriter:
        data = None
        config = None

        async def setup(self, config) -> None:
            self.config = config

        async def write(self, data) -> None:
            self.data = data

    stream = MockWriter()

    file_informer.file_store_service.files = {
        'default': {
            'data/abcd1234.jpg': b'BINARY_DATA'
        }
    }

    result = await file_informer.load(path, stream)

    assert stream.data == b'BINARY_DATA'
    assert stream.config is not None
    assert result is None


async def test_file_informer_load_not_found(file_informer):
    uri = 'nonexistent/xyz000.jpg'

    class MockWriter:
        async def setup(self, config) -> None:
            pass

        async def write(self, data) -> None:
            pass

    stream = MockWriter()

    with raises(MediaNotFoundError):
        result = await file_informer.load(uri, stream)
