from aiohttp import web
from rapidjson import dumps, loads
from typing import Any, Dict, Tuple
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import AudioSchema
from injectark import Injectark


class AudioResource:
    def __init__(self, injector: Injectark) -> None:
        self.injector = injector
        self.audio_storage_coordinator = self.injector[
            'AudioStorageCoordinator']
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
            'Total-Count': str(len(
                await self.mediark_reporter.search_audios(domain)))
        }

        return web.Response(headers=headers)

    async def get(self, request: web.Request) -> web.Response:
        """
        ---
        summary: Return all audios.
        tags:
          - Audios
        responses:
          200:
            description: "Successful response"
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Audio'
        """

        domain, limit, offset = get_request_filter(request)

        audios = AudioSchema().dump(
            await self.mediark_reporter.search_audios(domain), many=True)

        return web.json_response(audios, dumps=dumps)

    async def put(self, request: web.Request) -> web.Response:
        """
        ---
        summary: Create or update an audio.
        tags:
          - Audios
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Audio'
        responses:
          200:
            description: "Success"
        """
        many = True if request.query.get('many') else False
        data = AudioSchema(many=many).loads(await request.text())

        await self.audio_storage_coordinator.store(data)

        return web.Response(status=200)
