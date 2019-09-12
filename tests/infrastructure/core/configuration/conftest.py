import os
from json import dump
from pytest import fixture
from flask import Flask
from datetime import datetime
from typing import cast, List
from injectark import Injectark
from flask.testing import FlaskClient
from mediark.infrastructure.core import (
    build_config, build_factory, Config, JwtSupplier
)
from mediark.infrastructure.web import create_app
from uuid import uuid4


@fixture(scope='session')
def config_file(tmpdir_factory):
    config_file = str(tmpdir_factory.mktemp(
        'config').join('mediark_config.json'))

    data = {
        'domain': 'mediark.knowark.com',
        'media': '/var/opt/mediark/media',
        'shelve': '/var/opt/mediark/shelve'
    }

    with open(config_file, 'w') as f:
        dump(data, f)

    return config_file


@fixture
def app() -> Flask:
    """Create app testing client"""
    config = build_config("", os.environ.get('PROD', 'DEV'))

    # Configuration loading

    strategy = config['strategy']
    factory = build_factory(config)

    resolver = Injectark(strategy, factory)

    app = create_app(config, resolver)
    app.testing = True
    app = cast(Flask, app.test_client())

    return app


@fixture
def headers() -> dict:

    payload_dict = {
        "tid": "c5934df0-cab9-4660-af14-c95272a92ab7",
        "uid": "c4e47c69-b7ee-4a06-83bb-b59859478bec",
        "name": "John Doe",
        "email": "johndoe@nubark.com",
        "attributes": {},
        "authorization": {},
        "exp": int(datetime.now().timestamp()) + 5
    }

    jwt_supplier = JwtSupplier('knowark')
    token = jwt_supplier.encode(payload_dict)

    return {"Authorization": (token)}


@fixture
def retrieve_production_conf() -> Config:
    return build_config("", 'PROD')
