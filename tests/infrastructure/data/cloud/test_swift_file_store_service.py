from mediark.application.services import FileStoreService
from mediark.infrastructure.data import SwiftFileStoreService


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
    content, context = await swift_file_store_service.load(uri)

    assert content == b'BINARY_DATA'
    assert context == {
        'status': 200,
        'headers': {}
    }
