from ..config import Config
from .memory_factory import MemoryFactory
from .registry import Registry
from .types import ProviderList


class Resolver:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.factories = {
            'MemoryFactory': MemoryFactory(self.config)
        }

    def resolve(self, providers: ProviderList) -> Registry:
        return Registry()
