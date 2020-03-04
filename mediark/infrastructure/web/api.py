import asyncio
from typing import Dict, Any
from aiohttp import web
from apispec import APISpec
from injectark import Injectark
from .resources import (RootResource, ImageResource,
                        AudioResource, DownloadResource)
from .spec import create_spec


def create_api(app: web.Application, injector: Injectark) -> None:

    # API
    spec = create_spec()

    # Root Resource
    bind_routes(app, '/', RootResource(spec))

    # Images Resource
    bind_routes(app, "/images", ImageResource(injector))
    spec.path(path="/images", operations={
        'get': {}, 'post': {}, 'put': {}, 'head': {}}, resource=ImageResource)
    spec.path(path="/images/<id>", operations={
        'put': {}}, resource=ImageResource)

    # Audios Resource
    bind_routes(app, "/audios", AudioResource(injector))
    spec.path(path="/audios", operations={
        'get': {}, 'post': {}, 'head': {}}, resource=AudioResource)

    # Download Resource
    app.router.add_route(
        "get", "/download/{tenant}/{type}/{id_part_one}/{id_part_two}/{id}",
        getattr(DownloadResource(injector), "get", None))
    spec.path(path="/download",
              operations={'get': {}}, resource=DownloadResource)


def bind_routes(app: web.Application, path: str, resource: Any):
    general_methods = ['get', 'put', 'post', 'head', 'patch']
    identified_methods = ['get', 'put', 'delete', 'patch']
    for method in general_methods + identified_methods:
        handler = getattr(resource, method, None)
        if not handler:
            continue
        if method in identified_methods:
            app.router.add_route(method, path + "/{id}", handler)
        if method in general_methods:
            app.router.add_route(method, path, handler)
