from aiohttp import web
from typing import Callable, Type
from marshmallow import Schema
from ..helpers import get_request_filter, get_request_ids


class Resource:
    def __init__(self, schema: Type[Schema],
                 count_handler: Callable,
                 search_handler: Callable,
                 add_handler: Callable,
                 delete_handler: Callable) -> None:
        self.schema = schema
        self.count_handler = count_handler
        self.search_handler = search_handler
        self.add_handler = add_handler
        self.delete_handler = delete_handler

    async def head(self, request) -> web.Response:
        domain, _, _ = await get_request_filter(request)
        total_count = str(await self.count_handler(domain))
        return web.Response(headers={'Total-Count': total_count})

    async def get(self, request: web.Request) -> web.Response:
        domain, limit, offset = await get_request_filter(request)
        records = await self.search_handler(
            domain, limit=limit, offset=offset)
        result = self.schema().dump(records, many=True)
        return web.json_response(result)

    async def put(self, request: web.Request) -> web.Response:
        records = self.schema(
            many=True).loads(await request.text())
        await self.add_handler(records)
        return web.Response(status=200)

    async def post(self, request: web.Request) -> web.Response:
        records = self.schema(
            many=True).loads(await request.text())
        await self.add_handler(records)
        return web.Response(status=200)

    async def delete(self, request: web.Request) -> web.Response:
        ids = await get_request_ids(request)
        await self.delete_handler(ids)
        return web.Response(status=204)
