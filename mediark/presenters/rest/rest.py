import aiohttp_cors
import aiohttp_jinja2
from typing import Any
from pathlib import Path
from jinja2 import FileSystemLoader
from aiohttp import web, ClientSession
from injectark import Injectark
from ...core import Config
from .middleware import middlewares
from .doc import create_spec
from .resources import RootResource, MediaResource, DownloadResource


class RestApplication(web.Application):
    def __init__(self, config: Config, injector: Injectark) -> None:
        super().__init__(middlewares=middlewares(injector))
        self.config = config
        self.injector = injector
        self._setup()

    @staticmethod
    async def run(app: web.Application, port: int = 4321):
        await web._run_app(app, port=port)

    def _setup(self) -> None:
        templates = str(Path(__file__).parent / 'resources')
        aiohttp_jinja2.setup(self, loader=FileSystemLoader(templates))

        self.cleanup_ctx.append(self._http_client)
        cors = aiohttp_cors.setup(self, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*",
                allow_headers="*")})

        # API endpoints creation
        self._create_api()

        for route in list(self.router.routes()):
            cors.add(route)

    @staticmethod
    async def _http_client(app: web.Application):
        session = ClientSession()
        app['client'] = session
        yield
        await session.close()

    def _bind(self, path: str, resource: Any):
        general_methods = ['head', 'get', 'put', 'delete', 'post', 'patch']
        identified_methods = ['get', 'delete']
        for method in general_methods + identified_methods:
            handler = getattr(resource, method, None)
            if not handler:
                continue
            if method in identified_methods:
                self.router.add_route(method, path + "/{id}", handler)
            self.router.add_route(method, path, handler)

    def _create_api(self) -> None:
        # Restful API
        spec = create_spec()

        # Resources
        self._bind('/', RootResource(spec))
        self._bind('/medias', MediaResource(self.injector))
        self._bind('/downloads', DownloadResource(self.injector))
