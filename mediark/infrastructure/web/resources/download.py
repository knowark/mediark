from pathlib import Path
from typing import Any
from flask import request, jsonify, send_from_directory
from flask.views import MethodView
from marshmallow import ValidationError
from ..schemas import DownloadSchema
from ....application.utilities import TenantProvider


class DownloadResource(MethodView):
    def __init__(self, data_path: str, media_dir: str) -> None:
        self.data_path = data_path
        self.media_dir = media_dir

    def get(self, tenant: str, type: str, uri: str) -> Any:
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

        directory = Path(self.data_path).joinpath(
            tenant+"/"+self.media_dir+"/"+type)
        return send_from_directory(directory, uri)
