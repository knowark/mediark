"""
Mediark entrypoint
"""
import sys
import asyncio
import uvloop
from injectark import Injectark
from .presenters.shell import Shell
from .factories import factory_builder
from .core import config


async def main(args=None):  # pragma: no cover
    factory = factory_builder.build(config)
    injector = Injectark(factory)
    if config.get('auto'):
        injector['MigrationSupplier'].migrate()

    await Shell(config, injector).run(args or [])


if __name__ == '__main__':  # pragma: no cover
    uvloop.install()
    asyncio.run(main(sys.argv[1:]))
