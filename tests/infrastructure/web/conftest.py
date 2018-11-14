from pytest import fixture
from flask import Flask
from mediark.application.models import Image, Audio
from mediark.infrastructure.config import DevelopmentConfig
from mediark.infrastructure.resolver import Resolver, Registry
from mediark.infrastructure.web import create_app


def load_registry(registry: Registry) -> Registry:
    registry['ImageRepository'].load({
        "1": Image(id='1', reference='ABC'),
        "2": Image(id='2', reference='XYZ')
    })
    registry['AudioRepository'].load({
        "1": Audio(id='1', reference='ABC'),
        "2": Audio(id='2', reference='XYZ')
    })
    return registry


@fixture
def app() -> Flask:
    config = DevelopmentConfig()
    resolver = Resolver(config)
    providers = config['providers']
    registry = load_registry(resolver.resolve(providers))

    app = create_app(config, registry)
    app.testing = True
    app = app.test_client()

    return app
