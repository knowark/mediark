from functools import partial
from injectark import Injectark
from aiohttp import web, ClientSession


def setup_generators(app: web.Application, injector: Injectark):
    app.cleanup_ctx.append(partial(http_client, injector=injector))


async def http_client(app: web.Application, injector: Injectark):
    # Startup
    session = injector['HttpClientSupplier']
    app['client'] = session
    yield
    # Cleanup
    await session.close()
