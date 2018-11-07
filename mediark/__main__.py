import os
from .infrastructure.config import (
    DevelopmentConfig, MemoryRegistry, Config, Context)
from .infrastructure.web import create_app, ServerApplication


def main():  # pragma: no cover
    ConfigClass = DevelopmentConfig
    RegistryClass = MemoryRegistry

    config = ConfigClass()
    context = Context(config, RegistryClass(config))

    app = create_app(context)
    ServerApplication(app).run()


if __name__ == '__main__':  # pragma: no cover
    main()
