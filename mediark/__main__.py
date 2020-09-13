"""
Serproser entrypoint
"""
import sys
import asyncio
import uvloop
from injectark import Injectark
from .presenters.shell import Shell
from .factories import factory_builder, strategy_builder
from .core import config


async def main(args=None):
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)
    injector = Injectark(strategy=strategy, factory=factory)
    if config.get('auto'):
        injector['MigrationSupplier'].migrate()

    await Shell(config, injector).run(args or [])


if __name__ == '__main__':  # pragma: no cover
    uvloop.install()
    asyncio.run(main(sys.argv[1:]))
