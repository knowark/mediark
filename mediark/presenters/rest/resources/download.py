from typing import Any
from aiohttp import web
from injectark import Injectark


class DownloadResource:
    def __init__(self, injector: Injectark) -> None:
        self.file_informer = injector['FileInformer']

    async def get(self, request: web.Request) -> Any:
        uri = request.match_info.get('uri')
        response = web.Response()

        await response.prepare(request)
        response_dict = await self.file_informer.load(uri, response)

        return response
