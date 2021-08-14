from functools import partial
from injectark import Injectark
from aiohttp import web
from json import loads
from .resource import Resource
from ..helpers import get_request_ids
from .....integration.core.http import HttpBase64Reader
from .operations import operations


class MediaResource(Resource):
    def __init__(self, spec: dict, injector: Injectark) -> None:
        self.spec = spec
        self.informer = injector['StandardInformer']
        self.manager = injector['MediaStorageManager']
        self.paths = self.spec['paths']


    async def patch(self, request: web.Request) -> web.Response:
        records = loads(await request.text())
        meta, data = records['meta'], records['data']

        streams = [record.pop('data', None) for record in data]
        submission_records = [
            {'media': media, 'stream': stream and HttpBase64Reader(stream)}
            for media, stream in zip(data, streams)]
        medias = await self.manager.submit({
            "meta": meta,
            "data": submission_records
        })

        return web.json_response(medias)

    async def delete(self, request: web.Request) -> web.Response:
        ids = await get_request_ids(request)
        deletion_records = [{'id': id_} for id_ in ids]
        result = await self.manager.delete({
            "meta": {},
            "data": deletion_records
        })

        return web.json_response(result)

