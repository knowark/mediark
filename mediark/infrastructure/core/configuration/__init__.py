import json
from pathlib import Path
from json import load
from typing import Optional
from .config import *
from .development_config import *
from .production_config import *

def load_domain() -> str:
    domain = ''
    path_config = Path("/etc/opt/mediark/config.json")
    if not path_config.exists():
        return domain
    else:
        with open(path_config, 'r') as f:
            data = json.load(f) if f else ''
        return data['domain'] if data else ''

def build_config(config_path: str, mode: str) -> Config:
    if mode == 'DEV':
        return DevelopmentConfig()
    production_config = ProductionConfig()
    production_config['domain'] = load_domain()
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
