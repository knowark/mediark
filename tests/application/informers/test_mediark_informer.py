from mediark.application.informers.mediark_informer import (
    StandardMediarkInformer)
from pytest import fixture
from mediark.application.domain.models import Media
from mediark.application.informers import MediarkInformer
from mediark.application.domain.repositories import (
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
def mediark_informer(
        media_repository: MediaRepository) -> MediarkInformer:
    return StandardMediarkInformer(media_repository)


def test_mediark_informer_instantiation(mediark_informer):
    assert isinstance(mediark_informer, MediarkInformer)


async def test_mediark_informer_search_medias(
        mediark_informer: MediarkInformer) -> None:
    domain: QueryDomain = []
    medias = await mediark_informer.search('media', domain)
    assert len(medias) == 2


async def test_mediark_informer_count_medias(
        mediark_informer: MediarkInformer) -> None:
    medias_count = await mediark_informer.count('media')
    assert medias_count == 2
