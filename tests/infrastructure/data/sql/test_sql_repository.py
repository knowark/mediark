import rapidjson as json
from asyncio import sleep
from pathlib import Path
from pytest import fixture, raises
from asyncpg import connect
from filtrark import SqlParser, SafeEval
from mediark.application.reporters.types import QueryDomain
from mediark.application.models import Entity
from mediark.application.utilities import (
    QueryParser, EntityNotFoundError, StandardTenantProvider, Tenant,
    StandardAuthProvider, User)
from mediark.application.repositories import Repository
from mediark.infrastructure.data.sql import SqlRepository


class DummyEntity(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.id = attributes.get('id', '')
        self.field_1 = attributes.get('field_1', '')


def test_sql_repository_implementation() -> None:
    assert issubclass(SqlRepository, Repository)


@fixture
def sql_repository(connection_manager, dummies_table) -> SqlRepository:
    parser = SqlParser(SafeEval())
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id="001", name="Origin"))
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(id='001', name='johndoe'))

    sql_repository: SqlRepository = SqlRepository(
        table=dummies_table,
        constructor=DummyEntity,
        tenant_provider=tenant_provider,
        auth_provider=auth_provider,
        connection_manager=connection_manager,
        parser=parser)

    return sql_repository


def test_sql_repository_instantiation(sql_repository) -> None:
    assert sql_repository is not None


async def test_sql_repository_add(sql_repository):
    item = DummyEntity(
        id='eba4c8ee-3035-4f19-81ce-4ce21eb78b4c', field_1='value_5')

    await sql_repository.add(item)

    connection_manager = sql_repository.connection_manager
    connection_string = connection_manager.settings[0]['dsn']

    connection = await connect(connection_string)
    async with connection.transaction():
        result = await connection.fetch(
            f"SELECT data FROM origin.{sql_repository.table}")

    assert len(result) == 4
    assert any(json.loads(row['data'])['field_1'] == 'value_5'
               for row in result)


async def test_sql_repository_add_update(sql_repository):
    uid = '5fdda850-ac85-41e2-a105-f8b5ba593ecd'
    created_entity = DummyEntity(id=uid, field_1="value_99")
    created_entity, *_ = await sql_repository.add(created_entity)

    await sleep(1)

    updated_entity = DummyEntity(id=uid, field_1="New Value")
    updated_entity, *_ = await sql_repository.add(updated_entity)

    assert created_entity.created_at == updated_entity.created_at
    assert created_entity.created_by == updated_entity.created_by
    assert created_entity.updated_by == updated_entity.updated_by
    assert created_entity.updated_at != updated_entity.updated_at

    connection_manager = sql_repository.connection_manager
    connection_string = connection_manager.settings[0]['dsn']

    connection = await connect(connection_string)
    async with connection.transaction():
        result = await connection.fetch(
            f"""SELECT data FROM origin.{sql_repository.table}
                WHERE data->> 'id' = $1;""", uid)

    assert any(json.loads(row['data'])['field_1'] == 'New Value'
               for row in result)

    async with connection.transaction():
        result = await connection.fetch(
            f"""DELETE FROM origin.{sql_repository.table}
                WHERE data->> 'id' = $1;""", uid)


async def test_sql_repository_search(sql_repository):
    uid = 'f80fa6dd-29ff-4cb9-be5d-5952bc82decf'

    domain = [('field_1', '=', "value_2")]
    items = await sql_repository.search(domain)

    assert len(items) == 1
    assert items[0].id == uid
    assert items[0].field_1 == 'value_2'


async def test_sql_repository_search_in_ids(sql_repository):
    id_2 = 'f80fa6dd-29ff-4cb9-be5d-5952bc82decf'
    id_3 = 'a7c18b66-4bc9-41fc-9b4d-a137569f82b6'
    uid = 'f80fa6dd-29ff-4cb9-be5d-5952bc82decf'

    domain = [('id', 'in', [id_2, id_3])]
    items = await sql_repository.search(domain)

    assert len(items) == 2
    assert items[0].id == id_2
    assert items[1].id == id_3


async def test_sql_repository_limit(sql_repository):
    domain: QueryDomain = []
    items = await sql_repository.search(domain, limit=2)

    assert len(items) == 2


async def test_sql_repository_offset(sql_repository):
    domain: QueryDomain = []
    items = await sql_repository.search(domain, offset=2)
    uid = '99cc4dc3-4a6e-43a6-ae5f-1c126bf7c0c6'

    assert len(items) <= 2


async def test_sql_repository_search_limit_none(sql_repository):
    items = await sql_repository.search([], limit=None, offset=None)
    assert len(items) == 4


async def test_sql_repository_remove(sql_repository):
    item = DummyEntity(
        id='a7c18b66-4bc9-41fc-9b4d-a137569f82b6',
        field_1='value_3')

    await sql_repository.remove(item)

    connection_manager = sql_repository.connection_manager
    connection_string = connection_manager.settings[0]['dsn']

    connection = await connect(connection_string)
    async with connection.transaction():
        result = await connection.fetch(
            f"SELECT data FROM origin.{sql_repository.table}")

    assert not any(json.loads(row['data'])['id'] == item.id for row in result)


async def test_sql_repository_remove_empty(sql_repository):
    result = await sql_repository.remove([])
    assert result is False


async def test_sql_repository_remove_idempotent(sql_repository):
    existing_item = DummyEntity(
        id='328e094e-13ef-40ff-8252-b70d1d7fca6a',
        field_1='value_33')
    await sql_repository.add(existing_item)
    missing_item = DummyEntity(**{'id': 'missing', 'field_1': 'MISSING'})

    deleted = await sql_repository.remove(
        [existing_item, missing_item])

    assert deleted is True

    deleted = await sql_repository.remove(
        [existing_item, missing_item])

    assert deleted is False


async def test_sql_repository_remove_many(sql_repository):
    item_1 = DummyEntity(
        id='99cc4dc3-4a6e-43a6-ae5f-1c126bf7c0c6',
        field_1='value_1'
    )
    item_3 = DummyEntity(
        id='a7c18b66-4bc9-41fc-9b4d-a137569f82b6',
        field_1='value_3')

    items = [item_1, item_3]

    await sql_repository.remove(items)

    connection_manager = sql_repository.connection_manager
    connection_string = connection_manager.settings[0]['dsn']

    connection = await connect(connection_string)
    async with connection.transaction():
        result = await connection.fetch(
            f"SELECT data FROM origin.{sql_repository.table}")

    assert not any(
        json.loads(row['data'])['id'] == [item_1.id, item_3.id]
        for row in result)


async def test_sql_repository_count(sql_repository):
    domain = [('field_1', '=', "value_2")]
    count = await sql_repository.count(domain)

    assert count == 1
