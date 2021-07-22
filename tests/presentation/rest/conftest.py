from pytest import fixture
from injectark import Injectark
from mediark.integration.factories import factory_builder
from mediark.presentation.rest import RestApplication
from mediark.integration.core import config


@fixture
def app(loop, aiohttp_client):
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    app = RestApplication(config, injector)

    return loop.run_until_complete(aiohttp_client(app))


@fixture
def headers() -> dict:
    return {
        "Tenant": "Default",
        "From": "john@doe.com",
        "TenantId": "001",
        "UserId": "001",
        "Roles": "user"
    }
