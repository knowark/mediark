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
def load_registry():
    parser = QueryParser()
    tenant_service = StandardTenantProvider(Tenant(name="Origin"))
    image_repository = MemoryImageRepository(parser, tenant_service)
    image_repository.load({
        'default': {
            '001': Image(id='001', reference='ABC'),
            '002': Image(id='002', reference='XYZ')
        }
    })
    return image_repository


@fixture
def app() -> Flask:
    config = DevelopmentConfig()

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
    return build_config('', 'PROD')
