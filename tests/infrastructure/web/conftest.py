from flask import Flask
from pathlib import Path
from pytest import fixture
from datetime import datetime
from typing import cast, List
from injectark import Injectark
from mediark.application.models import Image, Audio
from mediark.application.utilities import QueryParser
from mediark.application.utilities.tenancy import (
    Tenant, StandardTenantProvider)
from mediark.application.repositories import (
    MemoryImageRepository, MemoryAudioRepository)
from mediark.infrastructure.core import (
    DevelopmentConfig, build_config, Config, JwtSupplier)
from mediark.infrastructure.core.factories import build_factory
from mediark.infrastructure.web import create_app, ServerApplication


@fixture
def mock_secret_file(tmp_path):
    mock_secret_file_path = str(tmp_path / "sign.txt")
    with open(mock_secret_file_path, "w") as f:
        f.write("123456")
    return str(mock_secret_file_path)


@fixture
def app(mock_secret_file) -> Flask:
    config = DevelopmentConfig()

    config['secrets'] = {
        "jwt": mock_secret_file
    }

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
        "tid": "1",
        "uid": "1",
        "name": "jjalvarez",
        "email": "jjalvarez@servagro.com.co",
        "attributes": {},
        "authorization": {},
        "exp": int(datetime.now().timestamp()) + 5
    }

    jwt_supplier = JwtSupplier('123456')
    token = jwt_supplier.encode(payload_dict)

    return {"Authorization": (token)}


@fixture
def retrieve_production_conf() -> Config:
    return build_config('', 'PROD')
