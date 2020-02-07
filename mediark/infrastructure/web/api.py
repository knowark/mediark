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

    # Middleware
    # authenticate = resolver['Authenticate']

    # Images Resource
    bind_routes(app, "/images", ImageResource(injector))
    spec.path(path="/images", operations={
        'get': {}, 'post': {}, 'head': {}}, resource=ImageResource)

    # Audios Resource
    bind_routes(app, "/audios", AudioResource(injector))
    spec.path(path="/audios", operations={
        'get': {}, 'post': {}, 'head': {}}, resource=AudioResource)

    # Download Resource
    app.router.add_route(
        "get", "/download/{tenant}/{type}/{uri}",
        getattr(DownloadResource, "get", None))

    # Audios Resource
    # spec.path(path="/audios", resource=AudioResource)
    # audio_view = authenticate(
    #     AudioResource.as_view('audios', resolver=resolver))
    # app.add_url_rule("/audios", view_func=audio_view)

    # # Download Resource
    # config_data = config['data']
    # spec.path(path="/download/<string:tenant>/<string:type>/<path:uri>",
    #           resource=DownloadResource)
    # download_view = DownloadResource.as_view('download', resolver=resolver)
    # app.add_url_rule(
    #     "/download/<string:tenant>/<string:type>/<path:uri>",
    #     view_func=download_view)

    # Download Resource
    # spec.path(path="/download/<string:tenant>/<string:type>/<path:uri>",
    #           resource=DownloadResource)
    # download_view = DownloadResource.as_view('download', resolver=resolver)
    # app.add_url_rule(
    #     "/download/<string:tenant>/<string:type>/<path:uri>",
    #     view_func=download_view)


def bind_routes(app: web.Application, path: str, resource: Any):
    general_methods = ['get', 'post', 'head', 'patch']
    identified_methods = ['get', 'put', 'delete', 'patch']
    for method in general_methods + identified_methods:
        handler = getattr(resource, method, None)
        if not handler:
            continue
        if method in identified_methods:
            app.router.add_route(method, path + "/{id}", handler)
        if method in general_methods:
            app.router.add_route(method, path, handler)
