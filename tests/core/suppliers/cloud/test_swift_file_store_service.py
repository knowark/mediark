from types import AsyncGeneratorType
from mediark.application.domain.services import FileStoreService
from mediark.core.suppliers import SwiftFileStoreService


def test_swift_file_store_service_instantiation(swift_file_store_service):
    assert isinstance(swift_file_store_service, FileStoreService)
    assert isinstance(swift_file_store_service, SwiftFileStoreService)


async def test_swift_file_store_service_store(swift_file_store_service):
    contexts = [{
        'id': 'f91bde0b-d094-45fd-bcf5-8cf24de853c0',
        'created_at': 1583933912,
        'content': b'BINARY_MEDIA_DATA'
    }]
    uri, *_ = await swift_file_store_service.store(contexts)

    assert uri == 'general/2020/03/11/f91bde0b-d094-45fd-bcf5-8cf24de853c0.txt'


async def test_swift_file_store_service_submit(swift_file_store_service):
    class MockStream:
        data = bytearray(b'AAABBBCCCDDD')
        chunk_size = 3
        offset = 0

        async def read(self, size) -> bytes:
            offset += self.chunk_size
            return self.data[i: i + self.chunk_size]

    mock_stream = MockStream()
    contexts = [{
        'id': 'f91bde0b-d094-45fd-bcf5-8cf24de853c0',
        'created_at': 1583933912,
        'stream': mock_stream
    }]
    uri, *_ = await swift_file_store_service.submit(contexts)

    client = swift_file_store_service.client

    assert uri == 'general/2020/03/11/f91bde0b-d094-45fd-bcf5-8cf24de853c0.txt'
    assert list(client.arguments['put'].keys()) == ['url', 'headers', 'data']
    assert client.arguments['put']['url'] == (
        'https://storage.bhs.cloud.ovh.net/v1/'
        'AUTH_e737167b6b424d92ae257f2d94bc1b83/'
        'custom-tenant-main/general/2020/03/11/'
        'f91bde0b-d094-45fd-bcf5-8cf24de853c0.txt')
    assert client.arguments['put']['headers'] == {
        'X-Auth-Token': 'AUTH_TOKEN_123'}
    assert isinstance(client.arguments['put']['data'], AsyncGeneratorType)


async def test_swift_file_store_service_generate_upload(
        swift_file_store_service):
    class MockStream:
        data = bytearray(b'AAABBBCCCDDD')
        chunk_size = 3
        offset = 0

        async def read(self, size) -> bytes:
            chunk = self.data[self.offset: self.offset + self.chunk_size]
            self.offset += self.chunk_size
            return chunk

    mock_stream = MockStream()

    generator = swift_file_store_service._generate_chunked_data(mock_stream)

    result = []
    async for chunk in generator:
        result.append(chunk)

    assert result == [b'AAA', b'BBB', b'CCC', b'DDD']


async def test_swift_file_store_service_make_url(swift_file_store_service):
    data_config = {
        'cloud': {
            'swift': {
                'object_store_url': 'https://storage.cloud',
                'container_prefix': 'north',
                'container_suffix': 'prod'
            }
        }
    }
    swift_file_store_service.data_config = data_config
    contexts = [{
        'id': 'f91bde0b-d094-45fd-bcf5-8cf24de853c0',
        'created_at': 1583933912
    }]
    uri = 'images/2020/02/15/5db7ec47-8bb1-4707-89c1-ad5aa76355e9.jpg'

    url = swift_file_store_service._make_url(uri)

    assert url == (
        'https://storage.cloud/north-custom-tenant-prod/'
        'images/2020/02/15/5db7ec47-8bb1-4707-89c1-ad5aa76355e9.jpg')


async def test_swift_file_store_service_load(swift_file_store_service):
    context = {
        'id': 'f91bde0b-d094-45fd-bcf5-8cf24de853c0',
        'created_at': 1583933912
    }
    uri = 'images/2020/02/15/5db7ec47-8bb1-4707-89c1-ad5aa76355e9.jpg'

    class MockWriter:
        async def write(self, data: bytes) -> None:
            self.data = data

    stream = MockWriter()

    result = await swift_file_store_service.load(uri, stream)

    assert stream.data == b'BINARY_DATA'
    assert result is None


async def test_swift_file_store_service_make_url_no_suffix(
        swift_file_store_service):
    data_config = {
        'cloud': {
            'swift': {
                'object_store_url': 'https://storage.cloud',
                'container_prefix': 'north',
            }
        }
    }
    swift_file_store_service.data_config = data_config
    contexts = [{
        'id': 'f91bde0b-d094-45fd-bcf5-8cf24de853c0',
        'created_at': 1583933912
    }]
    uri = 'images/2020/02/15/5db7ec47-8bb1-4707-89c1-ad5aa76355e9.jpg'

    url = swift_file_store_service._make_url(uri)

    assert url == (
        'https://storage.cloud/north-custom-tenant/'
        'images/2020/02/15/5db7ec47-8bb1-4707-89c1-ad5aa76355e9.jpg')
