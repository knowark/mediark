from pathlib import Path
from pytest import fixture
from json import dump
from injectark import Injectark
from mediark.infrastructure.core.configuration import (
    DevelopmentConfig, JsonConfig)


@fixture
def mock_development_config(tmp_path):
    mock_development_config = DevelopmentConfig()
    mock_development_config['tenancy']['json'] = str(tmp_path / 'tenants.json')
    mock_development_config['data']['dir_path'] = str(tmp_path / 'data')
    mock_development_config['secrets']['jwt'] = str(tmp_path / 'sign.txt')
    mock_development_config['secrets']['domain'] = str(tmp_path / 'domain.txt')
    with open(mock_development_config['secrets']['jwt'], "w") as f:
        f.write("123456")
    return mock_development_config


@fixture
def mock_production_config(mock_development_config):
    mock_production_config = JsonConfig()
    mock_production_config['tenancy']['json'] = \
        mock_development_config['tenancy']['json']
    mock_production_config['data']['dir_path'] = \
        mock_development_config['data']['dir_path']
    mock_production_config['secrets']['jwt'] = \
        mock_development_config['secrets']['jwt']
    mock_production_config['secrets']['domain'] = \
        mock_development_config['secrets']['domain']
    template_dir = Path(
        mock_production_config['data']['dir_path']) / "__template__"
    template_dir.mkdir(parents=True, exist_ok=True)
    (template_dir / "images").mkdir(parents=True, exist_ok=True)
    (template_dir / "audios").mkdir(parents=True, exist_ok=True)
    return mock_production_config


@fixture
def test_data(mock_development_config, mock_production_config):
    return [
        mock_development_config,
        mock_production_config
    ]
