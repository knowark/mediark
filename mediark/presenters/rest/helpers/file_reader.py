from aiohttp import BodyPartReader


class FileReader:
    def __init__(self, part: BodyPartReader) -> None:
        self.part = part

    async def read(size: int) -> bytes:
        return await self.part.read_chunk(size)
