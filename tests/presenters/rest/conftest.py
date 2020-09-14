
from pytest import fixture
from injectark import Injectark
from mediark.factories import strategy_builder, factory_builder
from mediark.presenters.rest import RestApplication
from mediark.core import config


@fixture
def app(loop, aiohttp_client):
    """Create app testing client"""
    config['factory'] = 'CheckFactory'
    #config['strategies'] = ['base', 'check']
    config['strategies'] = ['base', 'http', 'check']

    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

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


# import os
# from aiohttp import web
# from pathlib import Path
# from pytest import fixture
# from datetime import datetime
# from base64 import b64encode
# from typing import cast, List
# from injectark import Injectark
# from mediark.application.utilities import QueryParser, User
# from mediark.infrastructure.config import build_config, Config
# from mediark.infrastructure.factories import build_strategy, build_factory
# from mediark.infrastructure.web import create_app
# from migrark import sql_migrate


# @fixture
# def app(tmp_path, loop, aiohttp_client) -> web.Application:
#     config = build_config('DEV')
#     strategy = build_strategy(config['strategies'], config['strategy'])
#     factory = build_factory(config)

#     resolver = Injectark(strategy, factory)

#     app = create_app(config, resolver)

#     return loop.run_until_complete(aiohttp_client(app))


# @fixture
# def headers() -> dict:
#     return {
#         "TenantId": "001",
#         "UserId": "001"
#     }
