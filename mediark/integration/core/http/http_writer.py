from typing import Dict, Any
from aiohttp import web


class HttpResponseWriter:
    def __init__(self, response: web.StreamResponse) -> None:
        self.response = response

    async def setup(self, config: Dict[str, Any]) -> None:
        self.response.content_type = config['type']
        await self.response.prepare(self.response['request'])

    async def write(self, data: int) -> None:
        await self.response.write(data)
