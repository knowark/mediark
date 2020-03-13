from pytest import raises
from mediark.application.services import MemoryFileStoreService


def test_storage_coordinator_instantiation(media_storage_coordinator):
    assert media_storage_coordinator is not None


async def test_storage_coordinator_store_no_data(media_storage_coordinator):
    media_dict = [{
        'type': 'images',
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'extension': 'jpg'
    }]
    with raises(ValueError):
        await media_storage_coordinator.store(media_dict)


async def test_storage_coordinator_store_data(media_storage_coordinator):
    media_dict = [{
        'type': 'images',
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': 'QkFTRTY0X0RBVEE=',  # BASE64_DATA
        'extension': 'jpg'
    }]

    await media_storage_coordinator.store(media_dict)

    assert len(
        media_storage_coordinator.media_repository.data['default']) == 1


async def test_storage_coordinator_store_file(media_storage_coordinator):
    media_dict = [{
        'type': 'images',
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': ('"iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42'
                 'mNk+H+1noEIwDiqkL4KAUP4F0koL9m+AAAAAElFTkSuQmCC",'),
        'extension': 'png'
    }]

    await media_storage_coordinator.store(media_dict)

    assert len(
        media_storage_coordinator.media_repository.data) == 1


async def test_storage_coordinator_store_data_many(media_storage_coordinator):
    media_records = [
        {
            'type': 'images',
            'namespace': 'https://example.com',
            'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
            'data': 'QkFTRTY0X0RBVEE=',  # BASE64_DATA
            'extension': 'jpg'
        },
        {
            'type': 'images',
            'namespace': 'https://example.com',
            'reference': '546bc220-dec1-415d-9f25-53be060bfc7e',
            'data': 'T1RIRVJfQkFTRTY0X0RBVEE=',  # OTHER_BASE64_DATA
            'extension': 'jpg'
        }
    ]

    await media_storage_coordinator.store(media_records)

    assert len(
        media_storage_coordinator.media_repository.data['default']) == 2
