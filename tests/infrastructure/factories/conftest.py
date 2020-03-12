from pathlib import Path
from pytest import fixture
from json import dump
from injectark import Injectark
from mediark.infrastructure.core import DevelopmentConfig, ProductionConfig


@fixture
def mock_development_config(tmp_path):
    mock_development_config = DevelopmentConfig()
    mock_development_config['tenancy']['json'] = str(tmp_path / 'tenants.json')
    mock_development_config['data']['dir_path'] = str(tmp_path / 'data')
    return mock_development_config


@fixture
def mock_json_config(mock_development_config):
    mock_json_config = DevelopmentConfig()
    mock_json_config['tenancy']['json'] = (
        mock_development_config['tenancy']['json'])
    mock_json_config['data']['dir_path'] = (
        mock_development_config['data']['dir_path'])
    template_dir = Path(
        mock_json_config['data']['dir_path']) / "__template__"
    template_dir.mkdir(parents=True, exist_ok=True)
    (template_dir / "images").mkdir(parents=True, exist_ok=True)
    (template_dir / "audios").mkdir(parents=True, exist_ok=True)
    return mock_json_config


@fixture
def mock_directory_config(mock_development_config):
    mock_directory_config = DevelopmentConfig()
    mock_directory_config['factory'] = 'DirectoryFactory'
    mock_directory_config['strategies'] = ['base', 'directory']
    return mock_directory_config


@fixture
def test_data(mock_development_config,
              mock_json_config,
              mock_directory_config):
    return [
        mock_development_config,
        mock_json_config,
        mock_directory_config,
        ProductionConfig()
    ]
