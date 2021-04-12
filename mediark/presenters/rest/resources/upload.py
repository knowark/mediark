import multidict
from typing import Any
from aiohttp import web
from injectark import Injectark
from ..helpers import FileReader


class UploadResource:
    def __init__(self, injector: Injectark) -> None:
        self.manager = injector['MediaStorageManager']

    async def post(self, request):
        mulipart = await request.multipart()

        field = await mulipart.next()
        assert field.name == 'media'
        media = await field.json()

        field = await mulipart.next()
        assert field.name == 'file'
        stream = FileReader(field)
        submission = {'media': media, 'stream': stream}

        await self.manager.submit([submission])

        return web.Response()
