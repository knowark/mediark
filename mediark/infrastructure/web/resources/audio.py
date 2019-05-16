from typing import Any, Dict, Tuple
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from ..schemas import AudioSchema


class AudioResource(MethodView):

    def __init__(self, registry) -> None:
        self.audio_storage_coordinator = registry['audio_storage_coordinator']
        self.spec = registry['spec']

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Create audio.
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

        try:
            data = AudioSchema().loads(request.data or '{}')
        except ValidationError as error:
            return jsonify(code=400, error=error.messages), 400
        print('!!!!!!!!!!!!!!!!! DATA', data)
        audio = self.audio_storage_coordinator.store(data)
        print('##### audio', audio)
        # response = 'Audio Post: \n name<{0}> - locator<{1}>'.format(
        #     device.name,
        #     device.locator,
        # )

        # return response, 201
        return 201

    def get(self) -> Tuple[str, int]:
        """
        ---
        summary: Return all audios.
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

        try:
            data = AudioSchema().loads(request.data or '{}')
        except ValidationError as error:
            return jsonify(code=400, error=error.messages), 400
        audio = self.audio_storage_coordinator.store(data)
        
        return 201