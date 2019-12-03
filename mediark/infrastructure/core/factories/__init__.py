from typing import Dict, Any
from ..configuration import Config
from .factory import Factory
from .memory_factory import MemoryFactory
from .http_factory import HttpFactory
from .directory_factory import DirectoryFactory
from .json_factory import JsonFactory


def build_factory(config: Config):
    factory = config['factory']
    return {
        'MemoryFactory': lambda config: MemoryFactory(config),
        'HttpFactory': lambda config: HttpFactory(config),
        'JsonFactory': lambda config: JsonFactory(config),
        'DirectoryFactory': lambda config: DirectoryFactory(config),
    }[factory](config)
