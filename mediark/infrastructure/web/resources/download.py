from typing import Any, Dict, Tuple
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import DownloadSchema


class DownloadResource(MethodView):
    # def __init__(self) -> None:
            # self.image_storage_coordinator = resolver['ImageStorageCoordinator']
            # self.mediark_reporter = resolver['MediarkReporter']

    def get(self) -> Tuple[str, int]:
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

        # domain, limit, offset = get_request_filter(request)

        # images = ImageSchema().dump(
        #     self.mediark_reporter.search_images(domain), many=True)

        # return jsonify(images)
