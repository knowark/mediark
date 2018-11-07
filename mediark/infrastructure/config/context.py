from .config import Config
from .registry import Registry


class Context():
    def __init__(self, config: Config, registry: Registry) -> None:
        self.config = config
        self.registry = registry
