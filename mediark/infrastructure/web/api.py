from flask import Flask, jsonify
from injectark import Injectark
from .middleware import Authenticate
# from ..resolver import Registry
from .resources import (RootResource, ImageResource, AudioResource)
from .spec import create_spec


def create_api(app: Flask, resolver: Injectark) -> None:

    # Restful API
    spec = create_spec()

    # Root Resource (Api Specification)
    root_view = RootResource.as_view('root', spec=spec)
    app.add_url_rule("/", view_func=root_view)
    # Middleware
    authenticate = resolver['Authenticate']
    
    # Audio Resource
    spec.path(path="/audios", resource=AudioResource)
    audio_view = authenticate(AudioResource.as_view(
        'audios', resolver=resolver))
    app.add_url_rule("/audios", view_func=audio_view)

    # Image Resource
    spec.path(path="/images", resource=ImageResource)
    image_view = authenticate(ImageResource.as_view(
        'images', resolver=resolver))
    app.add_url_rule("/images", view_func=image_view)
