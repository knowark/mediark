import multidict
from typing import Any
from aiohttp import web
from injectark import Injectark


class UploadResource:
    def __init__(self, injector: Injectark) -> None:
        pass

    async def post(self, request):

        data = await request.post()

        color = data['color']
        foto = data['foto']

        foto_file = data['foto'].file

        print("-"*100)
        print("data      ----> ", data)
        print("color    ---->     ", color)
        print("foto    ---->     ", foto)
        print("foto    ---->     ", foto_file)
        print("-"*100)

        content = foto_file.read()

        return web.Response(body=content,
                            headers=multidict(
                                {'CONTENT-DISPOSITION': foto_file}))
