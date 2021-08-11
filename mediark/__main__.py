import sys
import asyncio
import uvloop
from injectark import Injectark
from .integration.core import config
from .integration.factories import factory_builder
from .presentation.system import Shell


async def main(args=None):  # pragma: no cover
    print("factory>>>>"*50)
    print(config)
    factory = factory_builder.build(config)
    print(factory)
    injector = Injectark(factory=factory)
    await Shell(injector).run(args or [])


if __name__ == '__main__':  # pragma: no cover
    uvloop.install()
    asyncio.run(main(sys.argv[1:]))
