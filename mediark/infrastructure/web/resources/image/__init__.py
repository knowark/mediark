from json import loads, decoder
from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource
from flasgger import swag_from
from ....web import SearchDomain


class ImageResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.image_storage_coordinator = kwargs['ImageStorageCoordinator']
        self.mediark_reporter = kwargs['MediarkReporter']

    @swag_from('get.yml')
    def get(self) -> str:
        domain = []  # type: SearchDomain
        query_filter = request.args.get('filter')

        if query_filter:
            try:
                domain = loads(query_filter)
            except decoder.JSONDecodeError:
                pass

        return self.mediark_reporter.search_images(domain)

    @swag_from('post.yml')
    def post(self) -> Tuple[str, int]:
        data = request.get_json()
        if not data:
            return '', 400
        self.image_storage_coordinator.store(data)
        ds = str(data)
        return ds, 200
