from mediark.application.services import MemoryFileStoreService


def test_storage_coordinator_instantiation(audio_storage_coordinator):
    assert audio_storage_coordinator is not None


async def test_storage_coordinator_store_no_data(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'extension': 'mp4'}
    await audio_storage_coordinator.store(audio_dict)

    assert len(audio_storage_coordinator.audio_repository.data) == 0


async def test_storage_coordinator_store_data(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': 'BASE64_DATA',
        'extension': 'mp4'
    }

    await audio_storage_coordinator.store(audio_dict)

    assert len(audio_storage_coordinator.audio_repository.data) == 1


async def test_storage_coordinator_store_file(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': ('"iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42'
                 'mNk+H+1noEIwDiqkL4KAUP4F0koL9m+AAAAAElFTkSuQmCC",'),
        'extension': 'png'
    }

    await audio_storage_coordinator.store(audio_dict)

    assert len(audio_storage_coordinator.audio_repository.data) == 1
