import json
from pathlib import Path
from json import load
from typing import Optional
from .config import Config, DevelopmentConfig, ProductionConfig


def build_config(mode: str, config_path: str = "") -> Config:
    if mode == 'DEV':
        return DevelopmentConfig()
    production_config: Config = ProductionConfig()
    loaded_config = load_config(config_path)
    if loaded_config is not None:
        production_config.update(loaded_config)
    return production_config


def load_config(config_path: str) -> Optional[Config]:
    path = Path(config_path)
    if not path.exists() or path.is_dir():
        return None

    with open(config_path) as f:
        return load(f)
