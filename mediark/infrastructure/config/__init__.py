from .config import Config, DevelopmentConfig


def build_config(config_path: str) -> Config:
    return DevelopmentConfig()
