from pytest import fixture
from injectark import Injectark
from mediark.infrastructure.core import (
    build_config,  DevelopmentConfig, setup_environment)
from mediark.infrastructure.factories import (
    build_factory, build_strategy)


@fixture
def mock_sql_migrator():
    class MockSqlMigrator:
        def migrate(self, *args, **kwargs):
            pass
    return MockSqlMigrator()


@fixture
def mock_config():
    config = build_config('', 'DEV')
    config['factory'] = 'SqlFactory'
    config['strategies'] = ['base', 'sql']
    return config


@fixture
def mock_injector(mock_config, mock_sql_migrator):
    strategy = build_strategy(
        mock_config['strategies'], mock_config['strategy'])
    factory = build_factory(mock_config)

    def sql_migrator(self):
        return mock_sql_migrator

    # setattr(factory, 'sql_migrator', sql_migrator)

    return Injectark(strategy, factory)


def test_setup_environment_sql(mock_config, mock_injector):
    result = setup_environment(mock_config, mock_injector)
