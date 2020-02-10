from aiohttp import web, ClientSession


def setup_generators(app: web.Application):
    app.cleanup_ctx.append(http_client)


async def http_client(app: web.Application):
    # Startup
    session = ClientSession()
    app['client'] = session
    yield
    # Cleanup
    await session.close()
