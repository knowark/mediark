from pathlib import Path
from json import load
from typing import Optional
from .config import *
from .development_config import *
from .production_config import *


def build_config(config_path: str, mode: str) -> Config:
    if mode == 'DEV':
        return DevelopmentConfig()

    production_config = ProductionConfig()
    loaded_config = load_config(config_path)
    if loaded_config is not None:
        production_config.update(loaded_config)

    return production_config


def load_config(config_path: str) -> Optional[Config]:
    path = Path(config_path)
    if not path.exists():
        path = Path(Path.home() / 'config.json')
        if not path.exists():
            return None

    with path.open() as f:
        return load(f)