from pytest import fixture
from mediark.application.domain.common import (
    QueryParser, Tenant, StandardTenantProvider, Tenant,
    AuthProvider, StandardAuthProvider, User, QueryDomain)
from mediark.application.domain.models import Media
from mediark.application.domain.services import MemoryFileStoreService
from mediark.application.domain.repositories import MemoryMediaRepository
from mediark.application.informers import FileInformer, StandardFileInformer


@fixture
def media_repository():
    parser = QueryParser()
    auth_provider = StandardAuthProvider()
    tenant_service = StandardTenantProvider()
    media_repository = MemoryMediaRepository(
        parser, tenant_service, auth_provider)
    media_repository.load({
        'default': {
            '001': Media(id='001', reference='ABC'),
            '002': Media(id='002', reference='XYZ')
        }
    })
    return media_repository


@fixture
def file_informer():
    file_store_service = MemoryFileStoreService(
        StandardTenantProvider(),
        StandardAuthProvider())
    return StandardFileInformer(file_store_service)


def test_file_informer_instantiation(file_informer):
    assert isinstance(file_informer, FileInformer)


async def test_file_informer_load(file_informer):
    uri = 'images/abcd1234.jpg'
    result = await file_informer.load(uri)
    assert isinstance(result, dict)
    assert result == {'body': b''}
