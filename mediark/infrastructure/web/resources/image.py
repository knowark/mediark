from aiohttp import web
from rapidjson import dumps, loads
from typing import Any, Dict, Tuple
from injectark import Injectark
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import ImageSchema


class ImageResource:

    def __init__(self, injector: Injectark) -> None:
        self.injector = injector
        self.image_storage_coordinator = self.injector[
            'ImageStorageCoordinator']
        self.mediark_reporter = self.injector['MediarkReporter']

    async def head(self, request: web.Request) -> web.Response:
        """
        ---
        summary: Return audios HEAD headers.
        tags:
          - Audios
        """

        domain, _, _ = get_request_filter(request)

        headers = {
            'Total-Count': str(await self.mediark_reporter.count(
                'images', domain))
        }

        return web.Response(headers=headers)

    async def get(self, request: web.Request) -> web.Response:
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
            await self.mediark_reporter.search_images(domain), many=True)

        return web.json_response(images, dumps=dumps)

    async def post(self, request: web.Request) -> web.Response:
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

        data = ImageSchema().loads(await request.text())
        await self.image_storage_coordinator.store(data)

        return web.Response(text="201 CREATED")
