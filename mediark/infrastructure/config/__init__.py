from .config import Config
from .development_config import DevelopmentConfig
from .production_config import ProductionConfig


def build_config(config_path: str, mode: str) -> Config:
    print('MODE ============', mode)
    if mode == 'DEV':
        return DevelopmentConfig()
    return ProductionConfig()
