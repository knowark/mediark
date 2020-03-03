from typing import Dict, Any
from ..core import Config
from .factory import Factory
from .directory_factory import DirectoryFactory
from .http_factory import HttpFactory
from .json_factory import JsonFactory
from .memory_factory import MemoryFactory
from .sql_factory import SqlFactory
from .check_factory import CheckFactory
from .cloud_factory import CloudFactory
from .strategies import build_strategy


def build_factory(config: Config) -> Factory:
    factory = config['factory']
    return {
        'MemoryFactory': lambda config: MemoryFactory(config),
        'JsonFactory': lambda config: JsonFactory(config),
        'SqlFactory': lambda config: SqlFactory(config),
        'HttpFactory': lambda config: HttpFactory(config),
        'DirectoryFactory': lambda config: DirectoryFactory(config),
        'CheckFactory': lambda config: CheckFactory(config),
        'CloudFactory': lambda config: CloudFactory(config)
    }[factory](config)
