from aiohttp import web
from typing import Callable, Type
from validark import normalize
from ..helpers import get_request_filter


class Resource:
    def __init__(self,
                 count_handler: Callable,
                 search_handler: Callable,
                 add_handler: Callable,
                 delete_handler: Callable) -> None:
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
        return web.json_response(normalize(records))
