from pytest import fixture
from injectark import Injectark
from mediark.integration.factories import factory_builder
from mediark.presentation.platform.rest import RestApplication
from mediark.integration.core import config


@fixture
def app(loop, aiohttp_client):
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    app = RestApplication(injector)

    return loop.run_until_complete(aiohttp_client(app))


@fixture
def headers() -> dict:
    return {
        # "Tenant": "Default",
        # "From": "john@doe.com",
        # "TenantId": "001",
        # "UserId": "001",
        # "Roles": "user"
        "Authorization":  (
            # Password: INTEGRARK_SECRET
            # Payload:
            # {
            #     "tid": "001",
            #     "uid": "001",
            #     "tenant": "Knowark",
            #     "name": "John Doe",
            #     "email": "john@doe.com"
            # }
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwMDEiLCJ1aWQiOi"
            "IwMDEiLCJ0ZW5hbnQiOiJLbm93YXJrIiwibmFtZSI6IkpvaG4gRG9lIiwiZW1ha"
            "WwiOiJqb2huQGRvZS5jb20ifQ.udlkUWVOatst5IoDRlJsQVn"
            "U_atCAltOelOJvRCr8BY"
        )

    }
