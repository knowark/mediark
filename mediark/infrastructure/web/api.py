from flask import Flask
from ..resolver import Registry
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
from .resources import ImageResource, MediaResource


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

    # Media Resource
    api.add_resource(MediaResource,
                     '/media/<string:type>/<path:uri>',
                     '/download/<string:type>/<path:uri>',
                     resource_class_kwargs={
                         'MEDIA_DIRECTORY': app.config['MEDIA']})

    return api
