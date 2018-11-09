from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource
from flasgger import swag_from


class AudioResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.audio_storage_coordinator = kwargs['AudioStorageCoordinator']
        self.mediark_reporter = kwargs['MediarkReporter']

    @swag_from('get.yml')
    def get(self) -> str:
        return self.mediark_reporter.search_audios([])

    @swag_from('post.yml')
    def post(self) -> Tuple[str, int]:
        data = request.get_json()
        if not data:
            return '', 400
        print('---- AUDIO >>>>', data)
        self.audio_storage_coordinator.store(data)
        ds = str(data)
        return ds, 200
