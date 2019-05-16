from flask import Flask, jsonify
from ..resolver import Registry
from .resources import (RootResource, ImageResource, AudioResource)
from .spec import create_spec


def create_api(app: Flask, registry: Registry) -> None:

    # Restful API
    spec = create_spec()
    registry['spec'] = spec

    # Root Resource (Api Specification)
    root_view = RootResource.as_view('root', registry=registry)
    app.add_url_rule("/", view_func=root_view)

    # Audio Resource
    spec.path(path="/audios/", resource=AudioResource)
    audio_view = AudioResource.as_view('audios', registry=registry)
    app.add_url_rule("/audios/", view_func=audio_view)

    # Image Resource
    spec.path(path="/images/", resource=ImageResource)
    image_view = ImageResource.as_view('images', registry=registry)
    app.add_url_rule("/images/", view_func=image_view)
