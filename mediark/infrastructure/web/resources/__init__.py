from flask import request, render_template, make_response, jsonify
from flask.views import MethodView
from .audio import AudioResource
from .image import ImageResource


class RootResource(MethodView):

    def __init__(self, registry) -> None:
        self.spec = registry.get('spec')

    def get(self) -> str:
        if 'api' in request.args:
            return jsonify(self.spec.to_dict())

        template = render_template('index.html', url="/?api")
        response = make_response(template, 200, {
            'Content-Type': 'text/html'
        })

        return response
