from flask import request, render_template, make_response, jsonify
from flask.views import MethodView
from .... import __version__
from .image import ImageResource
from .audio import AudioResource
# from .download import DownloadResource


class RootResource(MethodView):

    def __init__(self, spec) -> None:
        self.spec = spec

    def get(self) -> str:
        if 'api' in request.args:
            return jsonify(self.spec.to_dict())

        template = render_template(
            'index.html', url="/?api", version=__version__)
        response = make_response(template, 200, {
            'Content-Type': 'text/html'
        })

        return response
