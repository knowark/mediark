import psycopg2
from pytest import fixture


@fixture(scope='session')
def connection_database():
    user = 'mediark'
    password = user

    connection = psycopg2.connect(
        f"postgresql://{user}:{password}@localhost/postgres")
    connection.autocommit = True
    test_database = 'test_connection_database'
    with connection.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {test_database}")
        cursor.execute(f"CREATE DATABASE {test_database}")
    connection.close()

    return f'postgresql://{user}:{password}@localhost/{test_database}'
