from os import name
from pytest import fixture, raises
from mediark.core.http import HttpFileReader


async def test_http_file_reader():

    class MockBodyPartReader:
        data = bytearray(b'ABCD1234')

        async def read_chunk(self, size: int) -> bytes:
            return self.data[:size]

    mock_body_part_reader = MockBodyPartReader()

    reader = HttpFileReader(mock_body_part_reader)

    assert await reader.read(4) == b'ABCD'
