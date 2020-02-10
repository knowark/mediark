from typing import Dict, Any
from ..configuration import Config
from .factory import Factory
from .directory_factory import DirectoryFactory
from .http_factory import HttpFactory
from .json_factory import JsonFactory
from .memory_factory import MemoryFactory
from .sql_factory import SqlFactory


def build_factory(config: Config):
    factory = config['factory']
    return {
        'MemoryFactory': lambda config: MemoryFactory(config),
        'JsonFactory': lambda config: JsonFactory(config),
        'SqlFactory': lambda config: SqlFactory(config),
        'HttpFactory': lambda config: HttpFactory(config),
        'DirectoryFactory': lambda config: DirectoryFactory(config),
    }[factory](config)
