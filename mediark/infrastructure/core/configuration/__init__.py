import json
from pathlib import Path
from json import load
from typing import Optional
from .config import *
from .development_config import *
from .json_config import *
from .sql_config import *


def build_config(config_path: str, mode: str) -> Config:
    production_config: Config = SqlConfig()
    if mode == 'DEV':
        return DevelopmentConfig()
    elif mode == "JSON":
        production_config = JsonConfig()
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
