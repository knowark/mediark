import asyncio
from typing import Dict, Any
from aiohttp import web
from apispec import APISpec
from injectark import Injectark
from .resources import (RootResource, MediaResource, DownloadResource)
from .spec import create_spec


def create_api(app: web.Application, injector: Injectark) -> None:

    # API
    spec = create_spec()

    # Root Resource
    bind_routes(app, '/', RootResource(spec))

    # Media Resource
    bind_routes(app, "/media", MediaResource(injector))
    spec.path(path="/media", operations={
        'head': {}, 'get': {}, 'put': {}}, resource=MediaResource)

    # Download Resource
    app.router.add_route(
        "get", r'/download/{uri:(.*)}',
        getattr(DownloadResource(injector), "get", None))
    spec.path(path="/download", operations={
        'get': {}}, resource=DownloadResource)


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
