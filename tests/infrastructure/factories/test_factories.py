import inspect
from pytest import fixture, mark
from injectark import Injectark
from mediark.application.utilities.tenancy import Tenant
from mediark.infrastructure.factories import build_strategy, build_factory


def test_config(test_data):
    for config in test_data:
        factory = build_factory(config)
        strategy = build_strategy(config['strategies'], config['strategy'])
        resolver = Injectark(
            strategy=strategy, factory=factory)
        resolver["TenantProvider"].setup(Tenant(id="1", name="default"))

        for resource in config["strategy"].keys():
            result = resolver.resolve(resource)
            classes = inspect.getmro(type(result))
            assert resource in [item.__name__ for item in classes]
