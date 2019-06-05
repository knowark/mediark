from typing import Any, Dict, Tuple
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import AudioSchema


class AudioResource(MethodView):

    def __init__(self, resolver) -> None:
        self.audio_storage_coordinator = resolver['AudioStorageCoordinator']
        self.mediark_reporter = resolver['MediarkReporter']

    def get(self) -> Tuple[str, int]:
        """
        ---
        summary: Return all audios.
        tags:
          - Audios
        responses:
          200:
            description: "Successful response"
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Audio'
        """

        domain, limit, offset = get_request_filter(request)

        audios = AudioSchema().dump(
            self.mediark_reporter.search_audios(domain), many=True)

        return jsonify(audios)

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Register audio.
        tags:
          - Audios
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Audio'
        responses:
          201:
            description: "Audio created"
        """

        data = AudioSchema().loads(request.data)
        audio = self.audio_storage_coordinator.store(data)
        
        response = 'Audio Post: \n namespace<{0}>'.format(
            audio
        )

        return response, 201
