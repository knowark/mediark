import multidict
from typing import Any
from aiohttp import web
from injectark import Injectark
from .....integration.core.http import HttpFileReader


class UploadResource:
    def __init__(self, injector: Injectark) -> None:
        self.manager = injector['MediaStorageManager']

    async def put(self, request):
        mulipart = await request.multipart()

        field = await mulipart.next()
        assert field.name == 'media'
        media = await field.json()

        field = await mulipart.next()
        assert field.name == 'file'
        stream = HttpFileReader(field)
        submission = {'media': media, 'stream': stream}

        result = await self.manager.submit({
                "meta": {},
                "data": [submission]
                })

        return web.json_response(result)
