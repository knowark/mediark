import os
from flask import Flask
from pathlib import Path
from pytest import fixture
from datetime import datetime
from base64 import b64encode
from typing import cast, List
from injectark import Injectark
from mediark.application.models import Image, Audio
from mediark.application.utilities import QueryParser
from mediark.application.utilities.tenancy import (
    Tenant, StandardTenantProvider)
from mediark.application.repositories import (
    MemoryImageRepository, MemoryAudioRepository)
from mediark.infrastructure.core import (
    ProductionConfig, build_config, Config, JwtSupplier)
from mediark.infrastructure.core.factories import build_factory
from mediark.infrastructure.web import create_app, ServerApplication


@fixture
def app(tmp_path) -> Flask:
    config = ProductionConfig()

    mock_secret_file_path = str(tmp_path / "sign.txt")
    with open(mock_secret_file_path, "w") as f:
        f.write("123456")

    config['secrets'] = {
        "jwt": mock_secret_file_path,
        "domain": str(tmp_path / "domain.txt")
    }
    config['data']['dir_path'] = str(tmp_path / 'data')
    config['tenancy']['json'] = str(tmp_path / 'tenants.json')

    template_dir = Path(config['data']['dir_path']) / "__template__"
    template_dir.mkdir(parents=True, exist_ok=True)
    (template_dir / "images").mkdir(parents=True, exist_ok=True)
    (template_dir / "audios").mkdir(parents=True, exist_ok=True)

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
def encoded_image() -> str:
    filename = os.path.join(
        os.path.dirname(__file__), "assets/SampleImage.png")
    with open(filename, "rb") as f:
        binary_data = f.read()
    return str(b64encode(binary_data), "utf-8")


@fixture
def encoded_audio() -> str:
    filename = os.path.join(
        os.path.dirname(__file__), "assets/SampleAudio.mp3")
    with open(filename, "rb") as f:
        binary_data = f.read()
    return str(b64encode(binary_data), "utf-8")


@fixture
def retrieve_development_conf() -> Config:
    return build_config("", 'DEV')
