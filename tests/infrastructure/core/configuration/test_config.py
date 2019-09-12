from mediark.infrastructure.core import (
    load_config, build_config, ProductionConfig)


def test_load_config(config_file):
    result = load_config(config_file)
    assert result is not None
    assert isinstance(result, dict)


def test_load_config_missing_file(config_file):
    path = 'missing_config.json'
    result = load_config(path)
    assert result is None


def test_build_config_production(config_file):
    result = build_config(config_file, 'PROD')

    assert isinstance(result, ProductionConfig)
    assert result['domain'] == 'mediark.knowark.com'
    assert result['media'] == '/var/opt/mediark/media'
    assert result['shelve'] == '/var/opt/mediark/shelve'


def test_build_config_production_no_file():
    path = 'missing_config.json'
    result = build_config(path, 'PROD')

    assert isinstance(result, ProductionConfig)
    assert result['domain'] == 'http://0.0.0.0:8080'