from typing import Dict, Any
from injectark import FactoryBuilder
from .check_factory import CheckFactory
from .cloud_factory import CloudFactory
from .directory_factory import DirectoryFactory
from .http_factory import HttpFactory
from .memory_factory import MemoryFactory
from .sql_factory import SqlFactory
from .strategies import strategy_builder


factory_builder = FactoryBuilder([
    CheckFactory, CloudFactory, DirectoryFactory, HttpFactory, MemoryFactory,
    SqlFactory])

__all__ = [
    'strategy_builder',
    'factory_builder'
]


# from typing import Dict, Any
# from ..config import Config
# from .factory import Factory
# from .directory_factory import DirectoryFactory
# from .http_factory import HttpFactory
# from .memory_factory import MemoryFactory
# from .sql_factory import SqlFactory
# from .check_factory import CheckFactory
# from .cloud_factory import CloudFactory
# from .strategies import build_strategy


# def build_factory(config: Config) -> Factory:
#     factory = config['factory']
#     return {
#         'MemoryFactory': lambda config: MemoryFactory(config),
#         'SqlFactory': lambda config: SqlFactory(config),
#         'HttpFactory': lambda config: HttpFactory(config),
#         'DirectoryFactory': lambda config: DirectoryFactory(config),
#         'CheckFactory': lambda config: CheckFactory(config),
#         'CloudFactory': lambda config: CloudFactory(config)
#     }[factory](config)
