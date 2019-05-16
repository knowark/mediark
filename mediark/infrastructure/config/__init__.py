from .development_config import DevelopmentConfig
from .production_config import ProductionConfig
from .context import Context
from .registry import MemoryRegistry, ProductionRegistry, Registry

from json import load
from pathlib import Path
from .config import Config
# from .development_config import DevelopmentConfig
# from .production_config import ProductionConfig



def build_config(config_path: str, mode: str) -> Config:
    if mode == 'DEV':
        return DevelopmentConfig()

    production_config = ProductionConfig()
    loaded_config = load_config(config_path)
    if loaded_config is not None:
        production_config.update(loaded_config)

    return production_config


def load_config(config_path: str) -> Config:
    path = Path(config_path)
    if not path.exists():
        return None

    with open(config_path) as f:
        return load(f)
