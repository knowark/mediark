from ..config import Config
from .memory_factory import MemoryFactory
from .registry import Registry
from .types import ProviderDict, ProvidersDict


class Resolver:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.factories = {
            'MemoryFactory': MemoryFactory(self.config)
        }
        self.default_factory = self.config.get(
            'default_factory', 'MemoryFactory')

    def resolve(self, providers: ProvidersDict) -> Registry:
        providers = self._resolve_dependencies(providers)
        print('DEPENDENCIES_DICT', providers)

        registry = Registry()
        for name in providers.keys():
            if name in registry:
                continue
            self._build_instance(name, providers, registry)

        print('REGISTRY===>>>', registry)

        return registry

    def _resolve_dependencies(self, providers: ProvidersDict
                              ) -> ProvidersDict:

        for key, value in providers.items():
            factory = value.get('factory', self.default_factory)
            method = value.get('method')
            annotations = getattr(
                self.factories[factory], method).__annotations__
            providers[key]['dependencies'] = [
                value.__name__ for key, value in
                annotations.items() if key != 'return']

        return providers

    # def _build_registry(self, providers: ProvidersDict, current: str,
    #                     registry: Registry) -> None:
    #     provider = providers[current]
    #     dependencies = provider['dependencies']

    #     parameters = []
    #     for dependency in dependencies:
    #         parameters.append()

    #         instance = registry.get('')
    #         self._build_registry(providers, dependency, registry)
    #         break
    #     else:
    #         factory = provider.get('factory', self.default_factory)
    #         method = provider['method']
    #         registry[current] = getattr(self.factories[factory], method)()

    def _build_instance(self, name: str, providers: ProvidersDict,
                        registry: Registry) -> object:

        provider = providers['name']
        dependencies = provider['dependencies']

        arguments = []
        for dependency in dependencies:
            if dependency in registry:
                dependency_instance = registry[dependency]
            else:
                dependency_instance = self._build_instance(
                    dependency, dependencies, registry)
            arguments.append(dependency_instance)

        factory = provider.get('factory', self.default_factory)
        method = provider['method']

        instance = getattr(self.factories[factory], method)(*arguments)

        registry[name] = instance

        return instance
