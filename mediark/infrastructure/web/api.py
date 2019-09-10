from flask import Flask, jsonify
from injectark import Injectark
from .middleware import Authenticate
from .resources import (RootResource, ImageResource,
                        AudioResource, DownloadResource)
from .spec import create_spec
from ..core.configuration import Config


def create_api(app: Flask, resolver: Injectark) -> None:

    # API
    spec = create_spec()

    # Root Resource (Api Specification)
    root_view = RootResource.as_view('root', spec=spec)
    app.add_url_rule("/", view_func=root_view)

    # Middleware
    authenticate = resolver['Authenticate']

    # Images Resource
    spec.path(path="/images", resource=ImageResource)
    image_view = authenticate(
        ImageResource.as_view('images', resolver=resolver))
    app.add_url_rule("/images", view_func=image_view)

    # Audios Resource
    spec.path(path="/audios", resource=AudioResource)
    audio_view = authenticate(
        AudioResource.as_view('audios', resolver=resolver))
    app.add_url_rule("/audios", view_func=audio_view)

    # Download Resource
    spec.path(path="/download/<string:type>/<path:uri>",
              resource=DownloadResource)
    download_view = DownloadResource.as_view('download', config=Config())
    app.add_url_rule("/download/<string:type>/<path:uri>",
                     view_func=download_view)
