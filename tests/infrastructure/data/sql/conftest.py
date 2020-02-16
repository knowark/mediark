import rapidjson as json
import psycopg2
from pytest import fixture
from mediark.infrastructure.data.sql import DefaultConnectionManager


@fixture(scope='session')
def mediark_database():
    user = 'mediark'
    password = user

    connection = psycopg2.connect(
        f"postgresql://{user}:{password}@localhost/postgres")
    connection.autocommit = True
    test_database = 'test_mediark_database'
    with connection.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {test_database}")
        cursor.execute(f"CREATE DATABASE {test_database}")
    connection.close()

    return f'postgresql://{user}:{password}@localhost/{test_database}'


@fixture(scope='session')
def schema(mediark_database):
    user = 'mediark'
    password = user

    schema = 'origin'
    connection = psycopg2.connect(mediark_database)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(f'CREATE SCHEMA {schema};')
    connection.close()

    return schema


@fixture(scope='session')
def dummies_table(mediark_database, schema):
    connection = psycopg2.connect(mediark_database)
    connection.autocommit = True
    table = 'dummies'

    uid_1 = '99cc4dc3-4a6e-43a6-ae5f-1c126bf7c0c6'
    data_1 = json.dumps({
        'id': uid_1,
        'field_1': 'value_1'
    })
    uid_2 = 'f80fa6dd-29ff-4cb9-be5d-5952bc82decf'
    data_2 = json.dumps({
        'id': uid_2,
        'field_1': 'value_2'
    })
    uid_3 = 'a7c18b66-4bc9-41fc-9b4d-a137569f82b6'
    data_3 = json.dumps({
        'id': uid_3,
        'field_1': 'value_3'
    })
    with connection.cursor() as cursor:
        cursor.execute(
            f"CREATE TABLE {schema}.{table} ("
            "data JSONB)")
        cursor.execute(
            f"INSERT INTO {schema}.{table} "
            "(data) "
            "VALUES (%s)", (data_1,))
        cursor.execute(
            f"INSERT INTO {schema}.{table} "
            "(data) "
            "VALUES (%s)", (data_2,))
        cursor.execute(
            f"INSERT INTO {schema}.{table} "
            "(data) "
            "VALUES (%s)", (data_3,))
    connection.close()
    return table


@fixture
def connection_manager(mediark_database):
    settings = [{
        'name': 'default',
        'dsn': mediark_database,
        'max_size': 10
    }]
    return DefaultConnectionManager(settings)
