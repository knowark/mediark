import json
import aiohttp_jinja2
from typing import Any
from pathlib import Path
from jinja2 import FileSystemLoader
from aiohttp import web, ClientSession
from injectark import Injectark
from .middleware import middlewares
from .resources import (Resource,  RootResource,
        MediaResource, DownloadResource, UploadResource)

class RestApplication(web.Application):
    def __init__(self, injector: Injectark) -> None:
        super().__init__(middlewares=middlewares(injector))
        self.injector = injector
        self._setup()

    @staticmethod
    async def run(app: web.Application, port: int = 4321):
        await web._run_app(app, port=port)

    def _setup(self) -> None:
        templates = str(Path(__file__).parent / 'resources')
        aiohttp_jinja2.setup(self, loader=FileSystemLoader(templates))

        spec = json.loads(
            (Path(__file__).parent / 'openapi.json').read_text())

        self.cleanup_ctx.append(self._http_client)

        self.router.add_route(
            "get", r'/download/{tenant}/{path:(.*)}',
            getattr(DownloadResource(self.injector), "get", None))

        self.router.add_route(
            "post", '/upload',
            getattr(UploadResource(self.injector), "put", None))

        self.router.add_route(
            "put", '/upload',
            getattr(UploadResource(self.injector), "put", None))

        self.router.add_route(
            "patch", '/media',
            getattr(MediaResource(spec, self.injector), "patch", None))

        self.router.add_route(
            "patch", '/media/{id}',
            getattr(MediaResource(spec, self.injector), "patch", None))

        self.router.add_route(
            "delete", '/media',
            getattr(MediaResource(spec, self.injector), "delete", None))

        self.router.add_route(
            "delete", '/media/{id}',
            getattr(MediaResource(spec, self.injector), "delete", None))

        self._create_api(spec)

    @staticmethod
    async def _http_client(app: web.Application):
        session = ClientSession()
        app['client'] = session
        yield
        await session.close()

    def _create_api(self, spec) -> None:
        # spec = json.loads(
            # (Path(__file__).parent / 'openapi.json').read_text())

        resource = Resource(spec, self.injector)

        self.add_routes([
            web.get('/', RootResource(spec).get),

            web.get('/{resource}/{id}', resource.get, allow_head=False),

            web.get('/{resource}', resource.get, allow_head=False),

            web.head('/{resource}/{id}', resource.head),

            web.head('/{resource}', resource.head),

            web.patch('/{resource}/{id}', resource.patch),
            web.patch('/{resource}', resource.patch),

            web.delete('/{resource}/{id}', resource.delete),
            web.delete('/{resource}', resource.delete)
        ])

