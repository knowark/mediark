import shelve
from typing import Dict
from pytest import fixture
from mediark.application.repositories import Repository
from mediark.application.utilities import QueryParser
from mediark.infrastructure.data import ShelveRepository


class DummyEntity:
    def __init__(self, id: str, field_1: str) -> None:
        self.id = id
        self.field_1 = field_1


def test_shelve_repository_implementation() -> None:
    assert issubclass(ShelveRepository, Repository)


@fixture
def shelve_repository(dummy_shelve) -> ShelveRepository:
    with shelve.open(dummy_shelve) as items:
        items.clear()
    parser = QueryParser()
    entity_dict = {
        "1": DummyEntity('1', 'value_1'),
        "2": DummyEntity('2', 'value_2'),
        "3": DummyEntity('3', 'value_3')
    }
    print('dummy_shelve', dummy_shelve)
    repository = ShelveRepository[DummyEntity](parser, dummy_shelve)
    repository.load(entity_dict)
    return repository


def test_shelve_repository_get(shelve_repository) -> None:
    item = shelve_repository.get("1")

    assert item and item.field_1 == "value_1"


def test_shelve_repository_add(shelve_repository) -> None:
    item = DummyEntity("4", "value_4")

    is_saved = shelve_repository.add(item)
    assert is_saved

    with shelve.open(shelve_repository.filename) as items:
        assert len(items) == 4
        assert "4" in items.keys()
        assert items['4'].field_1 == item.field_1
        assert type(items['4']) == type(item)


def test_shelve_repository_search(shelve_repository):
    domain = [('field_1', '=', "value_3")]

    items = shelve_repository.search(domain)

    assert len(items) == 1
    for item in items:
        assert item.id == '3'
        assert item.field_1 == "value_3"


def test_shelve_repository_search_all(shelve_repository):
    items = shelve_repository.search([])

    assert len(items) == 3


def test_shelve_repository_search_limit(shelve_repository):
    items = shelve_repository.search([], limit=2)

    assert len(items) == 2


def test_shelve_repository_search_limit_zero(shelve_repository):
    items = shelve_repository.search([], limit=0)

    assert len(items) == 3


def test_shelve_repository_search_offset(shelve_repository):
    items = shelve_repository.search([], offset=2)

    assert len(items) == 1


def test_shelve_repository_remove_true(shelve_repository):
    with shelve.open(shelve_repository.filename, 'r') as items:
        item = items["2"]

    deleted = shelve_repository.remove(item)

    with shelve.open(shelve_repository.filename) as items:
        assert deleted is True
        assert len(items) == 2
        assert "2" not in items


def test_shelve_repository_remove_false(shelve_repository):
    item = DummyEntity(**{'id': '6', 'field_1': 'MISSING'})
    deleted = shelve_repository.remove(item)

    assert deleted is False

    with shelve.open(shelve_repository.filename, 'r') as items:
        assert len(items) == 3
