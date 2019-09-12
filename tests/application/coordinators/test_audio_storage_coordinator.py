from mediark.application.services import MemoryFileStoreService


def test_storage_coordinator_instantiation(audio_storage_coordinator):
    assert audio_storage_coordinator is not None


def test_storage_coordinator_store_no_data(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'extension': 'mp4'}
    audio_storage_coordinator.store(audio_dict)

    assert len(audio_storage_coordinator.audio_repository.data) == 0


def test_storage_coordinator_store_data(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': 'BASE64_DATA',
        'extension': 'mp4'
    }

    audio_storage_coordinator.store(audio_dict)

    assert len(audio_storage_coordinator.audio_repository.data) == 1


def test_storage_coordinator_store_file(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': ('"iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42'
                 'mNk+H+1noEIwDiqkL4KAUP4F0koL9m+AAAAAElFTkSuQmCC",'),
        'extension': 'png'
    }

    called = False

    class MockFileStoreService:
        def store(self, locator: str, content: str, extension: str = None):
            nonlocal called
            called = True
            file_store_service = MemoryFileStoreService()
            return file_store_service.store(locator, content, extension)

    audio_storage_coordinator.file_store_service = MockFileStoreService()
    audio_storage_coordinator.store(audio_dict)

    assert called is True
    audio = next(
        iter(audio_storage_coordinator.audio_repository.data.values()))
