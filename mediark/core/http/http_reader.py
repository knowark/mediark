from aiohttp import BodyPartReader
from base64 import b64decode


class HttpFileReader:
    def __init__(self, part: BodyPartReader) -> None:
        self.part = part

    async def read(self, size: int) -> bytes:
        return await self.part.read_chunk(size)


class Base64FileReader:
    def __init__(self, data: str) -> None:
        self.stream = b64decode(data)
        self.chunk_size = 512 * 1024
        self.offset = 0

    async def read(self, size: int) -> bytes:
        if size == -1:
            return self.stream
        chunk = self.stream[self.offset: self.offset + self.chunk_size]
        self.offset += self.chunk_size
        return chunk
