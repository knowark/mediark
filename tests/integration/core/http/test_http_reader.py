from os import name
from pytest import fixture, raises
from mediark.integration.core.http import HttpFileReader, HttpBase64Reader


async def test_http_file_reader():

    class MockBodyPartReader:
        data = bytearray(b'ABCD1234')

        async def read_chunk(self, size: int) -> bytes:
            return self.data[:size]

    mock_body_part_reader = MockBodyPartReader()

    reader = HttpFileReader(mock_body_part_reader)

    assert await reader.read(4) == b'ABCD'


async def test_http_base64_reader():
    base64data = 'SU1BR0VfREFUQQ=='
    reader = HttpBase64Reader(base64data)

    assert len(await reader.read(4)) == 4

    base64data = 'SU1BR0VfREFUQQ=='
    reader = HttpBase64Reader(base64data)

    assert len(await reader.read(-1)) == 10
