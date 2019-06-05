from flask import Flask, jsonify
from injectark import Injectark
from .middleware import Authenticate
from .resources import RootResource, ImageResource, AudioResource
from .spec import create_spec


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
    image_view = authenticate(ImageResource.as_view(
         'images', resolver=resolver))
    app.add_url_rule("/images", view_func=image_view)


    # Audios Resource
    spec.path(path="/audios", resource=AudioResource)
    audio_view = authenticate(AudioResource.as_view(
         'audios', resolver=resolver))
    app.add_url_rule("/audios", view_func=audio_view)

    # Download Resource
    # api.add_resource(DownloadResource,
    #                  '/download/<string:type>/<path:uri>',
    #                  resource_class_kwargs={
    #                      'MEDIA_DIRECTORY': app.config['MEDIA']})

