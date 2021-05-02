from functools import partial
from injectark import Injectark
from aiohttp import web
from .resource import Resource
from ..helpers import get_request_ids
from ....core.http import HttpBase64Reader


class MediaResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        self.informer = injector['MediarkInformer']
        self.manager = injector['MediaStorageManager']

        super().__init__(
            partial(self.informer.count, 'media'),
            partial(self.informer.search_media, 'media'),
            None,
            None)

    async def put(self, request: web.Request) -> web.Response:
        records = await request.json()
        streams = [record.pop('data', None) for record in records]

        submission_records = [
            {'media': media, 'stream': stream and HttpBase64Reader(stream)}
            for media, stream in zip(records, streams)]

        await self.manager.submit(submission_records)

        return web.Response(status=200)

    async def delete(self, request: web.Request) -> web.Response:
        ids = await get_request_ids(request)
        deletion_records = [{'id': id_} for id_ in ids]
        await self.manager.delete(deletion_records)

        return web.Response(status=200)
