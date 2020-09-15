from pytest import fixture
from injectark import Injectark
from mediark.core import config
from mediark.presenters.shell import Shell
from mediark.factories import factory_builder, strategy_builder


@fixture
def shell() -> Shell:
    config['factory'] = 'MemoryFactory'
    config['strategies'] = ['base']

    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

    return Shell(config, injector)
