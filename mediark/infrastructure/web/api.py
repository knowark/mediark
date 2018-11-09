from flask import Flask
from ..resolver import Registry
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
from .resources import ImageResource, AudioResource, DownloadResource


def create_api(app: Flask, registry: Registry) -> Api:

    # REST API
    api = Api(app)

    # Swagger
    Swagger(app, template_file="api.yml", config={
        "specs_route": "/",
        "headers": [],
        "specs": [{
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True
    })

    # Images Resource
    api.add_resource(ImageResource, '/images',
                     resource_class_kwargs=registry)

    # Audios Resource
    api.add_resource(AudioResource, '/audios',
                     resource_class_kwargs=registry)

    # Download Resource
    api.add_resource(DownloadResource,
                     '/download/<string:type>/<path:uri>',
                     resource_class_kwargs={
                         'MEDIA_DIRECTORY': app.config['MEDIA']})

    return api
