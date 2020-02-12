from rapidjson import dump, loads
from pathlib import Path
from pytest import fixture, raises
from mediark.application.models import Entity
from mediark.application.utilities import (
    QueryParser, EntityNotFoundError, StandardTenantProvider, Tenant,
    StandardAuthProvider, User)
from mediark.application.repositories import Repository
from mediark.infrastructure.data import JsonRepository


class DummyEntity(Entity):
    def __init__(self, id: str = '', field_1: str = '') -> None:
        self.id = id
        self.field_1 = field_1


def test_json_repository_implementation() -> None:
    assert issubclass(JsonRepository, Repository)


@fixture
def json_repository(tmp_path) -> JsonRepository:
    item_dict = {
        "1": vars(DummyEntity('1', 'value_1')),
        "2": vars(DummyEntity('2', 'value_2')),
        "3": vars(DummyEntity('3', 'value_3'))
    }
    collection = 'dummies'
    tenant_directory = tmp_path / "default" / 'json'
    tenant_directory.mkdir(parents=True)
    file_path = str(tenant_directory / f'{collection}.json')

    with open(file_path, 'w') as f:
        dump({collection: item_dict}, f, indent=2)

    parser = QueryParser()
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(
        id="3",
        name="Default",
        zone=str(tmp_path)
    ))
    auth_provider = StandardAuthProvider(User(
        id='001', name='johndoe'))

    json_repository = JsonRepository(
        parser=parser, tenant_provider=tenant_provider,
        auth_provider=auth_provider, collection=collection,
        item_class=DummyEntity)

    return json_repository


async def test_json_repository_get(json_repository):
    item = await json_repository.get("1")
    assert item and item.field_1 == "value_1"


async def test_json_repository_get_not_found(json_repository):
    with raises(EntityNotFoundError):
        await json_repository.get("99")


async def test_json_repository_add(json_repository):
    item = DummyEntity('5', 'value_5')
    await json_repository.add(item)

    with json_repository._file_path.open() as f:
        data = loads(f.read())
        items = data.get("dummies")

        item_dict = items.get('5')

        assert item_dict.get('field_1') == item.field_1


def test_json_repository_add_no_id(json_repository) -> None:
    item = DummyEntity(field_1='value_5')
    item = json_repository.add(item)

    file_path = str(json_repository._file_path)
    with open(file_path) as f:
        data = loads(f.read())
        items = data.get("dummies")
        for key in items:
            assert len(key) > 0


async def test_json_repository_update(json_repository) -> None:
    updated_entity = DummyEntity("1", "New Value")

    is_updated = await json_repository.update(updated_entity)

    file_path = str(json_repository._file_path)
    with open(file_path) as f:
        data = loads(f.read())
        items = data.get("dummies")

        assert len(items) == 3
        assert is_updated is True
        assert "New Value" in items['1']['field_1']


async def test_json_repository_update_false(json_repository):
    missing_entity = DummyEntity("99", "New Value")

    is_updated = await json_repository.update(missing_entity)

    file_path = str(json_repository._file_path)
    with open(file_path) as f:
        data = loads(f.read())
        items = data.get("dummies")

        assert len(items) == 3
        assert is_updated is False


async def test_json_repository_search(json_repository):
    domain = [('field_1', '=', "value_3")]
    items = await json_repository.search(domain)

    assert len(items) == 1
    for item in items:
        assert item.id == '3'
        assert item.field_1 == "value_3"


async def test_json_repository_search_all(json_repository):
    items = await json_repository.search([])
    assert len(items) == 3


async def test_json_repository_search_limit(json_repository):
    items = await json_repository.search([], limit=2)
    assert len(items) == 2


async def test_json_repository_search_limit_none(json_repository):
    items = await json_repository.search([], limit=None, offset=None)
    assert len(items) == 3


async def test_json_repository_search_offset(json_repository):
    items = await json_repository.search([], offset=2)
    assert len(items) == 1


async def test_json_repository_remove_true(json_repository):
    file_path = str(json_repository._file_path)
    with open(file_path) as f:
        data = loads(f.read())
        items_dict = data.get("dummies")
        item_dict = items_dict.get('2')

    item = DummyEntity(**item_dict)
    deleted = await json_repository.remove(item)

    with open(file_path) as f:
        data = loads(f.read())
        items_dict = data.get("dummies")

    assert deleted is True
    assert len(items_dict) == 2
    assert "2" not in items_dict.keys()


async def test_json_repository_remove_false(json_repository):
    file_path = str(json_repository._file_path)
    item = DummyEntity(**{'id': '6', 'field_1': 'MISSING'})
    deleted = await json_repository.remove(item)

    with open(file_path) as f:
        data = loads(f.read())
        items_dict = data.get("dummies")

    assert deleted is False
    assert len(items_dict) == 3
