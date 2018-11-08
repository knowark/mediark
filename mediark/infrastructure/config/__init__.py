from .config import Config
from .development_config import DevelopmentConfig


def build_config(config_path: str) -> Config:
    return DevelopmentConfig()
