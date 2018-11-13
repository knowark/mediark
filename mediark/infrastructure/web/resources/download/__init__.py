from pathlib import Path
from typing import Any
from flask import send_from_directory
from flask_restful import Resource
from flasgger import swag_from


class DownloadResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.media_directory = kwargs['MEDIA_DIRECTORY']

    @swag_from('get.yml')
    def get(self, type: str, uri: str) -> Any:
        directory = Path(self.media_directory).joinpath(type)
        headers = {'Content-type': 'application/octet-stream'}
        return send_from_directory(directory, uri), 200, headers
