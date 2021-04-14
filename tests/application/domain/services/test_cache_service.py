import time
from pytest import fixture, raises
from mediark.application.domain.common import (
    StandardTenantProvider, Tenant)
from mediark.application.domain.services import (
    CacheService, StandardCacheService)


def test_cache_service() -> None:
    methods = CacheService.__abstractmethods__  # type: ignore
    assert 'get' in methods
    assert 'set' in methods


@fixture
def cache():
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="Default"))

    return StandardCacheService(tenant_provider)


def test_cache_service_set_get(cache) -> None:
    cache.set('co', 'Colombia')

    value = cache.get('co')

    assert value == 'Colombia'
    assert cache.get('en', 'England') == 'England'


def test_cache_service_least_recently_used(cache) -> None:
    cache.size = 3

    cache.set('ar', 'Argentina')
    cache.set('br', 'Brazil')
    cache.set('co', 'Colombia')
    cache.set('ec', 'Ecuador')

    assert cache.get('ec', '') == 'Ecuador'
    assert cache.get('co', '') == 'Colombia'
    assert cache.get('br', '') == 'Brazil'
    assert cache.get('ar', '') == ''


def test_cache_service_raises_on_not_found(cache) -> None:
    cache.size = 3

    with raises(KeyError):
        assert cache.get('co')


def test_cache_service_expiration(cache) -> None:
    cache.size = 3
    cache.lifetime = 0.01

    cache.set('ar', 'Argentina')

    time.sleep(0.02)

    assert cache.get('ar', '') == ''
