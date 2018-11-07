from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource
from flasgger import swag_from


class ImageResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.image_storage_coordinator = kwargs['image_storage_coordinator']
        self.mediark_reporter = kwargs['mediark_reporter']

    @swag_from('get.yml')
    def get(self) -> str:
        return self.mediark_reporter.search_images([])

    @swag_from('post.yml')
    def post(self) -> Tuple[str, int]:
        data = request.get_json()
        self.image_storage_coordinator.store(data)
        ds = str(data)
        return ds, 200
