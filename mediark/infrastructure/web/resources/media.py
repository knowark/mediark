from aiohttp import web
from rapidjson import dumps, loads
from typing import Any, Dict, Tuple
from injectark import Injectark
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import MediaSchema


class MediaResource:

    def __init__(self, injector: Injectark) -> None:
        self.injector = injector
        self.media_storage_coordinator = self.injector[
            'MediaStorageCoordinator']
        self.mediark_reporter = self.injector['MediarkReporter']

    async def head(self, request: web.Request) -> web.Response:
        """
        ---
        summary: Return medias HEAD headers.
        tags:
          - Media
        """

        domain, _, _ = get_request_filter(request)

        headers = {
            'Total-Count': str(len(
                await self.mediark_reporter.search_media(domain)))
        }

        return web.Response(headers=headers)

    async def get(self, request: web.Request) -> web.Response:
        """
        ---
        summary: Return all medias.
        tags:
          - Media
        responses:
          200:
            description: "Successful response"
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Media'
        """

        domain, limit, offset = get_request_filter(request)

        medias = MediaSchema().dump(
            await self.mediark_reporter.search_media(domain), many=True)

        return web.json_response(medias, dumps=dumps)

    async def put(self, request: web.Request) -> web.Response:
        """
        ---
        summary: Create or update an media.
        tags:
          - Media
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Media'
        responses:
          200:
            description: "Success"
        """
        media_records = MediaSchema(many=True).loads(await request.text())

        await self.media_storage_coordinator.store(media_records)

        return web.Response(status=200)
