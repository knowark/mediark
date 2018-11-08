from ..config import Config
from .memory_factory import MemoryFactory
from .types import ProviderDict, ProvidersDict, ProvidersList, Registry


class Resolver:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.factories = {
            'MemoryFactory': MemoryFactory(self.config)
        }
        self.default_factory = self.config.get('factory', 'MemoryFactory')

    def resolve(self, providers: ProvidersDict) -> Registry:
        providers_list = self._resolve_dependencies(providers)

        registry = {}  # type: Registry
        for provider in providers_list:
            if provider['name'] in registry:
                continue
            self._resolve_instance(provider, registry)

        return registry

    def _resolve_dependencies(self, providers: ProvidersDict
                              ) -> ProvidersList:

        for key, value in providers.items():
            factory = value.get('factory', self.default_factory)
            method = value.get('method')
            annotations = getattr(
                self.factories[factory], method).__annotations__
            providers[key]['name'] = key
            providers[key]['dependencies'] = [
                providers[value.__name__] for key, value in
                annotations.items() if key != 'return']

        return list(providers.values())

    def _resolve_instance(self, provider: ProviderDict,
                          registry: Registry) -> object:

        arguments = []
        for dependency in provider['dependencies']:
            if dependency['name'] in registry:
                dependency_instance = registry[dependency['name']]
            else:
                dependency_instance = self._resolve_instance(
                    dependency, registry)
            arguments.append(dependency_instance)

        factory = provider.get('factory', self.default_factory)
        method = provider['method']
        name = provider['name']

        instance = getattr(self.factories[factory], method)(*arguments)
        registry[name] = instance

        return instance
