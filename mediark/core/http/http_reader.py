from aiohttp import BodyPartReader


class HttpFileReader:
    def __init__(self, part: BodyPartReader) -> None:
        self.part = part

    async def read(self, size: int) -> bytes:
        return await self.part.read_chunk(size)
