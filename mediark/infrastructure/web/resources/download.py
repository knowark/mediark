from typing import Any
from aiohttp import web
from injectark import Injectark


class DownloadResource:
    def __init__(self, injector: Injectark) -> None:
        self.file_reporter = injector['FileReporter']

    async def get(self, request: web.Request) -> Any:
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

        uri = request.match_info.get('uri')
        response_dict = await self.file_reporter.load(uri)
        return web.Response(**response_dict)
