from pytest import raises, fixture
from pathlib import Path
from base64 import b64decode


@fixture
def base_path(directory_file_store_service):
    base_path = Path("{0}/{1}/{2}".format(
        directory_file_store_service.data_config["dir_path"],
        directory_file_store_service.tenant_service.tenant.slug,
        directory_file_store_service.data_config["media"]["dir_path"]))
    return base_path


async def test_directory_file_store_service_submit(
        directory_file_store_service, base_path):

    class MockStream:
        data = bytearray(b'AAABBBCCCDDD')
        chunk_size = 3
        offset = 0

        async def read(self, size) -> bytes:
            chunk = self.data[self.offset: self.offset + self.chunk_size]
            self.offset += self.chunk_size
            return chunk

    mock_stream = MockStream()
    id_ = "abca8e11-0719-44ab-bd3f-ed5aa1bd2918"
    extension = "png"
    data_type = 'images'

    contexts = [{
        'id': id_,
        'created_at': 1583964551,
        'type': data_type,
        'extension': extension,
        'stream': mock_stream
    }]

    uri, *_ = await directory_file_store_service.submit(contexts)

    image_path = base_path / uri

    assert image_path.is_file()
    assert uri == "images/2020/03/11/abca8e11-0719-44ab-bd3f-ed5aa1bd2918.png"
    assert image_path.read_bytes() == b'AAABBBCCCDDD'


async def test_directory_file_store_service_load(
        directory_file_store_service, base_path):

    class MockStream:
        data = bytearray(b'AAABBBCCCDDD')
        chunk_size = 3
        offset = 0

        async def read(self, size) -> bytes:
            chunk = self.data[self.offset: self.offset + self.chunk_size]
            self.offset += self.chunk_size
            return chunk

    mock_read_stream = MockStream()
    id_ = "abca8e11-0719-44ab-bd3f-ed5aa1bd2918"
    extension = "png"
    data_type = 'images'

    contexts = [{
        'id': id_,
        'created_at': 1583964551,
        'type': data_type,
        'extension': extension,
        'stream': mock_read_stream
    }]

    class MockWriter:
        async def write(self, data: bytes) -> None:
            self.data = data

    stream = MockWriter()

    uri, *_ = await directory_file_store_service.submit(contexts)

    await directory_file_store_service.load(uri, stream)

    assert stream.data == b'AAABBBCCCDDD'


async def test_directory_file_store_service_delete(
        directory_file_store_service, base_path):

    class MockStream:
        data = bytearray(b'AAABBBCCCDDD')
        chunk_size = 3
        offset = 0

        async def read(self, size) -> bytes:
            chunk = self.data[self.offset: self.offset + self.chunk_size]
            self.offset += self.chunk_size
            return chunk

    mock_read_stream = MockStream()
    id_ = "abca8e11-0719-44ab-bd3f-ed5aa1bd2918"
    extension = "png"
    data_type = 'images'

    contexts = [{
        'id': id_,
        'created_at': 1583964551,
        'type': data_type,
        'extension': extension,
        'stream': mock_read_stream
    }]

    class MockWriter:
        async def write(self, data: bytes) -> None:
            self.data = data

    stream = MockWriter()

    uri, *_ = await directory_file_store_service.submit(contexts)

    image_path = base_path / uri

    assert image_path.exists()
    assert image_path.read_bytes() == b'AAABBBCCCDDD'

    await directory_file_store_service.delete(uri)

    assert not image_path.exists()
