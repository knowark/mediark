from pathlib import Path
from typing import Any
from flask import request, jsonify, send_from_directory
from flask.views import MethodView
from marshmallow import ValidationError
from ..schemas import DownloadSchema


class DownloadResource(MethodView):

    def __init__(self, **kwargs: Any) -> None:
        self.media_directory = kwargs['config']['media']
        self.kwargs = kwargs

    def get(self, type:str, uri:str) -> Any:
        """
        ---
        summary: Return all media.
        tags:
          - Download
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

        directory = Path(self.media_directory).joinpath(type)
        return send_from_directory(directory, uri)