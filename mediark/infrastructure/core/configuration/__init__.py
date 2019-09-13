import json
from pathlib import Path
from json import load
from typing import Optional
from .config import *
from .directory_config import *
from .shelve_config import *
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
    if not path.exists() or path.is_dir():
        return None

    with open(config_path) as f:
        return load(f)
