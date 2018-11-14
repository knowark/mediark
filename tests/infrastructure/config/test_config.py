from mediark.infrastructure.config import (
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
    assert result['download'] == 'mediark.knowark.com/download'
    assert result['environment']['media'] == '/var/opt/mediark/media'
    assert result['environment']['shelve'] == '/var/opt/mediark/shelve'


def test_build_config_production_no_file():
    path = 'missing_config.json'
    result = build_config(path, 'PROD')

    assert isinstance(result, ProductionConfig)
    assert result['download'] == result['domain'] + '/download'
    assert result['environment']['media'] == result['home'] + '/media'
    assert result['environment']['shelve'] == result['home'] + '/shelve'
