from pytest import raises
from mediark.application.services import MemoryFileStoreService


def test_storage_coordinator_instantiation(image_storage_coordinator):
    assert image_storage_coordinator is not None


async def test_storage_coordinator_store_no_data(image_storage_coordinator):
    image_dict = [{
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'extension': 'jpg'
    }]
    with raises(ValueError):
        await image_storage_coordinator.store(image_dict)


async def test_storage_coordinator_store_data(image_storage_coordinator):
    image_dict = [{
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': 'QkFTRTY0X0RBVEE=',  # BASE64_DATA
        'extension': 'jpg'
    }]

    await image_storage_coordinator.store(image_dict)

    assert len(
        image_storage_coordinator.image_repository.data['default']) == 1


async def test_storage_coordinator_store_file(image_storage_coordinator):
    image_dict = [{
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': ('"iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42'
                 'mNk+H+1noEIwDiqkL4KAUP4F0koL9m+AAAAAElFTkSuQmCC",'),
        'extension': 'png'
    }]

    await image_storage_coordinator.store(image_dict)

    assert len(
        image_storage_coordinator.image_repository.data) == 1


async def test_storage_coordinator_store_data_many(image_storage_coordinator):
    image_records = [
        {
            'namespace': 'https://example.com',
            'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
            'data': 'QkFTRTY0X0RBVEE=',  # BASE64_DATA
            'extension': 'jpg'
        },
        {
            'namespace': 'https://example.com',
            'reference': '546bc220-dec1-415d-9f25-53be060bfc7e',
            'data': 'T1RIRVJfQkFTRTY0X0RBVEE=',  # OTHER_BASE64_DATA
            'extension': 'jpg'
        }
    ]

    await image_storage_coordinator.store(image_records)

    assert len(
        image_storage_coordinator.image_repository.data['default']) == 2
