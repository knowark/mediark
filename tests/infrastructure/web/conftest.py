import os
from aiohttp import web
from pathlib import Path
from pytest import fixture
from datetime import datetime
from base64 import b64encode
from typing import cast, List
from injectark import Injectark
from mediark.application.models import Image, Audio
from mediark.application.utilities import QueryParser, User
from mediark.application.repositories import (
    MemoryImageRepository, MemoryAudioRepository)
from mediark.infrastructure.core import (
    SqlConfig, build_config, Config)
from mediark.infrastructure.core.factories import build_factory
from mediark.infrastructure.web import create_app
from migrark import sql_migrate


@fixture
def xapp(tmp_path, loop, aiohttp_client) -> web.Application:
    # config = build_config('config.json', "JSON")
    config = build_config('config.json', "PROD")

    config['domain'] = 'https://mediark.dev.nubark.cloud'
    config['data']['dir_path'] = str(tmp_path / 'data')
    config['tenancy']['json'] = str(tmp_path / 'tenants.json')

    template_dir = Path(config['data']['dir_path']) / "__template__"
    template_dir.mkdir(parents=True, exist_ok=True)

    (template_dir / "json").mkdir(parents=True, exist_ok=True)
    (template_dir / "json" / "audios.json").write_text('{"audios":{}}')
    (template_dir / "json" / "images.json").write_text('{"images":{}}')
    (template_dir / 'media' / "images").mkdir(parents=True, exist_ok=True)
    (template_dir / 'media' / "audios").mkdir(parents=True, exist_ok=True)

    strategy = config['strategy']
    factory = build_factory(config)

    resolver = Injectark(strategy, factory)

    tenant_supplier = resolver["TenantSupplier"]

    tenant_zone = ""

    if config["mode"] == "JSON":
        tenant_zone = config['data']['dir_path']
    else:
        database_uri = config['zones']['default']['dsn']
        migrations_path = str((
            Path(__file__).parent.parent.parent.parent / 'mediark' /
            'infrastructure' / 'data' / 'sql' / 'migrations'
        ).absolute())
        sql_migrate(database_uri, migrations_path, schema='test',
                    target_version="004")

    try:
        resolver["TenantSupplier"].create_tenant({
            'id': "001", "name": "Test", "zone": tenant_zone})
    except Exception:
        resolver["AuthProvider"].setup(User(id='001', name='johndoe'))

    app = create_app(config, resolver)

    return loop.run_until_complete(aiohttp_client(app))


@fixture
def app(tmp_path, loop, aiohttp_client) -> web.Application:
    config = build_config('', 'TEST')
    strategy = config['strategy']
    factory = build_factory(config)
    print('\n\n\n\Factory:::', factory)

    resolver = Injectark(strategy, factory)

    app = create_app(config, resolver)

    return loop.run_until_complete(aiohttp_client(app))


@fixture
def headers() -> dict:
    return {
        "TenantId": "001",
        "UserId": "001"
    }


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
