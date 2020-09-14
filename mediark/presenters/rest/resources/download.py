
from functools import partial
from injectark import Injectark
from ..helpers.schemas import MediaSchema
from ..helpers import missing
from .resource import Resource


class DownloadResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['FileInformer']

        super().__init__(
            MediaSchema,
            missing,
            partial(informer.load, 'media'),
            missing,
            missing)

# from typing import Any
# from aiohttp import web
# from injectark import Injectark


# class DownloadResource:
#     def __init__(self, injector: Injectark) -> None:
#         self.file_informer = injector['FileInformer']

#     async def get(self, request: web.Request) -> Any:
#         """
#         ---
#         summary: Return all media.
#         tags:
#           - Download
#         responses:
#           200:
#             description: "Successful response"
#         """

#         uri = request.match_info.get('uri')
#         response_dict = await self.file_informer.load(uri)
#         return web.Response(**response_dict)
