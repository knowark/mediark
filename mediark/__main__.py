import os
from .infrastructure.config import Config, build_config
from .infrastructure.resolver import Resolver
from .infrastructure.cli import Cli


def main():  # pragma: no cover
    mode = os.environ.get('MEDIARK_MODE', 'PROD')
    config_path = os.environ.get('MEDIARK_CONFIG', 'mediark_config.json')
    config = build_config(config_path, mode)

    resolver = Resolver(config)
    providers = config['providers']
    registry = resolver.resolve(providers)

    Cli(config, registry)


if __name__ == '__main__':  # pragma: no cover
    main()
