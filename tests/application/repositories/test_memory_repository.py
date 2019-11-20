from typing import Dict
from pytest import fixture, raises
from mediark.application.repositories import MemoryRepository
from mediark.application.repositories import Repository
from mediark.application.utilities.tenancy import (
    Tenant, StandardTenantProvider)
from mediark.application.utilities import QueryParser, EntityNotFoundError


class DummyEntity:
    def __init__(self, id: str = "", field_1: str = "") -> None:
        self.id = id
        self.field_1 = field_1


@fixture
def filled_memory_repository(memory_repository) -> MemoryRepository:
    data_dict = {
        "default": {
            "1": DummyEntity('1', 'value_1'),
            "2": DummyEntity('2', 'value_2'),
            "3": DummyEntity('3', 'value_3')
        }
    }
    memory_repository.load(data_dict)
    return memory_repository


def test_memory_repository_implementation() -> None:
    assert issubclass(MemoryRepository, Repository)


@fixture
def memory_repository() -> MemoryRepository:
    tenant_service = StandardTenantProvider(Tenant(name="Default"))
    parser = QueryParser()
    repository: MemoryRepository = MemoryRepository(
        parser=parser, tenant_service=tenant_service)
    repository.load({"default": {}})
    return repository


def test_memory_repository_get(filled_memory_repository) -> None:
    item = filled_memory_repository.get("1")
    # item = filled_memory_repository.data['default'].get('1')


def test_memory_repository_get_missing(filled_memory_repository) -> None:
    with raises(EntityNotFoundError):
        filled_memory_repository.get("999999999")


def test_memory_repository_add(filled_memory_repository) -> None:
    parser = QueryParser()
    tenant_service = StandardTenantProvider(Tenant(name="Default"))
    repository: MemoryRepository = MemoryRepository(
        parser=parser, tenant_service=tenant_service)
    item = DummyEntity("1", "value_1")
    is_saved = repository.add(item)

    assert len(repository.data) == 1
    assert is_saved
    assert "1" in repository.data['default'].keys()
    assert item in repository.data['default'].values()


def test_memory_repository_search(filled_memory_repository):
    domain = [('field_1', '=', "value_3")]

    items = filled_memory_repository.search(domain)
    assert len(items) == 1
    for item in items:
        assert item.id == '3'
        assert item.field_1 == "value_3"


def test_memory_repository_search_all(filled_memory_repository):
    items = filled_memory_repository.search([])

    assert len(items) == 3


def test_memory_repository_search_limit(filled_memory_repository):
    items = filled_memory_repository.search([], limit=2)

    assert len(items) == 2


def test_memory_repository_search_limit_zero(filled_memory_repository):
    items = filled_memory_repository.search([], limit=0)

    assert len(items) == 3


def test_memory_repository_search_offset(filled_memory_repository):
    items = filled_memory_repository.search([], offset=2)

    assert len(items) == 1


def test_memory_repository_remove_true(filled_memory_repository):
    item = filled_memory_repository.data['default']['2']
    deleted = filled_memory_repository.remove(item)
    items = filled_memory_repository.data['default']
    assert deleted is True
    assert len(items) == 2
    assert "2" not in items


def test_memory_repository_remove_false(filled_memory_repository):
    item = DummyEntity(**{'id': '6', 'field_1': 'MISSING'})
    deleted = filled_memory_repository.remove(item)
    items = filled_memory_repository.data['default']
    assert deleted is False
    assert len(items) == 3
