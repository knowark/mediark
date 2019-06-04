from typing import Dict, Any
from ..configuration import Config
from .factory import Factory
from .memory_factory import MemoryFactory
from .http_factory import HttpFactory
from .directory_factory import DirectoryFactory
from .shelve_factory import ShelveFactory

def build_factory(config: Config) -> Factory:
    factory = config['factory']
    return {
        'MemoryFactory': lambda config: MemoryFactory(config),
        'HttpFactory': lambda config: HttpFactory(config),
        'DirectoryFactory': lambda config: DirectoryFactory(MemoryFactory),
        'ShelveFactory': lambda config: ShelveFactory(MemoryFactory),
    }[factory](config)
