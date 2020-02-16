from mediark.infrastructure.core import (
    load_config, build_config, JsonConfig)


def test_load_config(config_file):
    result = load_config(config_file)
    assert result is not None
    assert isinstance(result, dict)


def test_load_config_missing_file(config_file):
    path = 'missing_config.json'
    result = load_config(path)
    assert result is None


def test_build_config_production(config_file):
    result = build_config(config_file, 'JSON')

    assert isinstance(result, JsonConfig)


def test_build_config_production_no_file():
    path = 'missing_config.json'
    result = build_config(path, 'JSON')

    assert isinstance(result, JsonConfig)
