from pathlib import Path
from typing import Any
from flask import send_from_directory
from flask_restful import Resource
from flasgger import swag_from


class MediaResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.media_directory = kwargs['MEDIA_DIRECTORY']

    @swag_from('get.yml')
    def get(self, type: str, uri: str) -> str:
        directory = Path(self.media_directory).joinpath(type)
        return send_from_directory(directory, uri)
