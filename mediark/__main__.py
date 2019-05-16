import os
from .infrastructure.web import create_app, ServerApplication
# from .infrastructure.config import build_config
from .infrastructure.config import (
    DevelopmentConfig, ProductionRegistry, MemoryRegistry, Context)
# from .infrastructure.resolver import Resolver
# from .infrastructure.cli import Cli


def main():  # pragma: no cover
    ConfigClass = DevelopmentConfig  # type: Type[Config]
    RegistryClass = ProductionRegistry  # type: Type[Registry]

    # mode = os.environ.get('MEDIARK_MODE', 'PROD')
    # config_path = os.environ.get('MEDIARK_CONFIG', 'mediark_config.json')
    
    # config = build_config(config_path, mode)

    # resolver = Resolver(config)
    # providers = config['providers']
    # registry = resolver.resolve(providers)
    # Cli(config, registry)

    config = ConfigClass()
    context = Context(config, RegistryClass(config))
    gunicorn_config = config['gunicorn']

    app = create_app(context)
    ServerApplication(app, gunicorn_config).run()


if __name__ == '__main__':  # pragma: no cover
    main()
