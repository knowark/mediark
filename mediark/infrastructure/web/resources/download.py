import requests
from ast import literal_eval
from typing import Any, Dict, Tuple
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import DownloadSchema


class DownloadResource(MethodView):
    def __init__(self, resolver) -> None:
        self.mediark_reporter = resolver['MediarkReporter']

    def get(self) -> Tuple[str, int]:
        """
        ---
        summary: Return all media.
        tags:
          - Downloads
        responses:
          200:
            description: "Successful response"
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Download'
        """
        
        data = DownloadSchema().loads(request.data)
        reference = data['reference']
        type_media = data['type']
        domain = [('reference','=', reference)]
        if type_media == 'audio':
          audios = DownloadSchema().dump(
              self.mediark_reporter.search_audios(domain), many=True)
          return jsonify(audios) if audios else jsonify([])
        else:
          images = DownloadSchema().dump(
              self.mediark_reporter.search_images(domain), many=True)
          return jsonify(images) if images else jsonify([])
