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
        
        reference = '"349ab3b0-2abc-4e7b-af4d-73ccefeb905d"'
        domain = [('reference','=', reference)]
        audio = DownloadSchema().dump(
            self.mediark_reporter.search_audios(domain), many=True)
        url_audio = 'https://mediark.nubark.cloud/audios?filter=[["reference","=",'
        request_audio = url_audio + reference + ']]'
        audio_request = requests.get(request_audio)
        if audio_request.status_code == 200:
            r_audio = audio_request.text
        file_audio = literal_eval(r_audio)
        return jsonify(file_audio[0]['url'])
