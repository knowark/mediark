from typing import Tuple
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import ImageSchema


class ImageResource(MethodView):
    
    def __init__(self, resolver) -> None:
        self.image_storage_coordinator = resolver['ImageStorageCoordinator']
        self.mediark_reporter = resolver['MediarkReporter']

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Register image.
        tags:
          - images
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Image'
        responses:
          201:
            description: "image created"
        """

        data = ImageSchema().loads(request.data)

        image = self.image_storage_coordinator.store(data)
        
        response = 'image Post: \n name<{0}> - code<{1}>'.format(
            image.namespace,
            image.reference,
        )

        return response, 201
        

    def get(self) -> Tuple[str, int]:
        """
        ---
        summary: Return all images.
        tags:
          - images
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