from typing import Any, Dict, Tuple
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import ImageSchema


class ImageResource(MethodView):

    def __init__(self, resolver) -> None:
        self.image_storage_coordinator = resolver['ImageStorageCoordinator']
        self.mediark_reporter = resolver['MediarkReporter']

    def get(self) -> Tuple[str, int]:
        """
        ---
        summary: Return all images.
        tags:
          - Images
        responses:
          200:
            description: "Successful response"
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Image'
        """

        domain, limit, offset = get_request_filter(request)

        images = ImageSchema().dump(
            self.mediark_reporter.search_images(domain), many=True)

        return jsonify(images)

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Register image.
        tags:
          - Images
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Image'
        responses:
          201:
            description: "Image created"
        """

        data = ImageSchema().loads(request.data)

        image = self.image_storage_coordinator.store(data)
        
        response = 'Image Post: \n name<{0}> - code<{1}>'.format(
            image.id,
            image.namespace,
        )

        return response, 201
