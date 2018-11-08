import os
# from .infrastructure.config import build_context
from .infrastructure.config import Config, build_config
from .infrastructure.resolver import Resolver, Registry
from .infrastructure.web import create_app, ServerApplication
from .infrastructure.cli import cli


def main():  # pragma: no cover
    # ConfigClass = DevelopmentConfig
    # RegistryClass = MemoryRegistry

    # config = ConfigClass()
    # context = Context(config, RegistryClass(config))
    # gunicorn_config = config['gunicorn']
    config_path = os.environ.get('MEDIARK_CONFIG', 'mediark_config.json')

    config = build_config(config_path)

    resolver = Resolver(config)

    providers = config['providers']

    print('PROVIDERS', providers)

    registry = resolver.resolve(providers)

    print('REGISTRY', registry)

    # app = create_app(context)

    # ServerApplication(app, gunicorn_config).run()

    # Cli(config)


if __name__ == '__main__':  # pragma: no cover
    main()
