"""
Mediark entrypoint
"""
import os
import sys
import uvloop
import asyncio
import uvloop
from injectark import Injectark
from .infrastructure.config import build_config
from .infrastructure.factories import build_strategy, build_factory
from .infrastructure.cli import Cli


async def main(args=None):  # pragma: no cover
    mode = os.environ.get('MEDIARK_MODE', 'PROD')
    config_path = os.environ.get('MEDIARK_CONFIG', 'config.json')
    config = build_config(mode, config_path)

    factory = build_factory(config)
    strategy = build_strategy(config['strategies'], config['strategy'])
    injector = Injectark(strategy=strategy, factory=factory)
    injector['SetupSupplier'].setup()

    await Cli(config, injector).run(args or [])


if __name__ == '__main__':  # pragma: no cover
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1:]))
    loop.close()
