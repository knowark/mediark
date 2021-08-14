from mediark.application.operation.informers import StandardInformer
from pytest import fixture
from mediark.application.domain.models import Media
from mediark.application.domain.services.repositories import (
    RepositoryService,
    MediaRepository, MemoryMediaRepository)
from mediark.application.domain.common import (
    QueryParser, StandardTenantProvider, Tenant,
    AuthProvider, StandardAuthProvider, User, QueryDomain)


@fixture
def parser():
    return QueryParser()


@fixture
def auth_provider() -> AuthProvider:
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(id='001', name='johndoe'))
    return auth_provider


@fixture
def tenant_provider():
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="Default"))
    return tenant_provider


@fixture
def media_repository(
        tenant_provider, auth_provider, parser) -> MediaRepository:
    media_repository = MemoryMediaRepository(
        parser, tenant_provider, auth_provider)
    media_repository.load({
        'default': {
            '1': Media(**{'id': '1', 'name': "Conjunto Altagracia"}),
            '2': Media(**{'id': '2', 'name': "Alcaldía de Kyskta"}),
        }
    })
    return media_repository


@fixture
def repository_service(media_repository):
    return RepositoryService([media_repository])


@fixture
def standard_informer(repository_service)-> StandardInformer:
    return StandardInformer(repository_service)


def test_standard_informer_instantiation(standard_informer):
    assert isinstance(standard_informer, StandardInformer)


async def test_standard_informer_search_medias(
        standard_informer: StandardInformer) -> None:
    domain: QueryDomain = []
    medias = await standard_informer.search({
        'meta':{
            'model': 'Media',
            'domain':domain
       }
    })
    assert len(medias['data']) == 2


async def test_standard_informer_count_medias(
        standard_informer: StandardInformer) -> None:
    medias_count = await standard_informer.count({
        'meta':{
            'model':'Media',
            'domain':[]
        }
    })
    assert medias_count['data'] == 2
