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
        
        data = request.data
        if data:
            data['media'] == 'audio'

        audio = DownloadSchema().dump(
            self.mediark_reporter.search_audio(data['reference']))
        return jsonify(audio)
