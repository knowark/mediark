from typing import Tuple
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from ..schemas import ImageSchema


class ImageResource(MethodView):
    
    def __init__(self, registry) -> None:
        self.image_storage_coordinator = registry['image_storage_coordinator']
        self.spec = registry['spec']

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Create image.
        tags:
          - Images
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Images'
        responses:
          201:
            description: "Image created"
        """

        try:
            data = ImageSchema().loads(request.data or '{}')
        except ValidationError as error:
            return jsonify(code=400, error=error.messages), 400
        image = self.image_storage_coordinator.store(data)
        print('Image', image)
        # response = 'Audio Post: \n name<{0}> - locator<{1}>'.format(
        #     device.name,
        #     device.locator,
        # )

        # return response, 201
        return 201