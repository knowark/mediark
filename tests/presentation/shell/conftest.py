from pytest import fixture
from injectark import Injectark
from mediark.integration.core import config
from mediark.presentation.shell import Shell
from mediark.integration.factories import factory_builder


@fixture
def shell() -> Shell:
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    return Shell(config, injector)
