from pytest import fixture
from mediark.application.repositories import (
    MemoryAudioRepository)
from mediark.application.utilities.expression_parser import ExpressionParser
from mediark.application.services import (
    StandardIdService, MemoryFileStoreService)
from mediark.application.coordinators import AudioStorageCoordinator


@fixture
def audio_storage_coordinator():
    parser = ExpressionParser()
    audio_repository = MemoryAudioRepository(parser)
    id_service = StandardIdService()
    file_store_service = MemoryFileStoreService()

    return AudioStorageCoordinator(
        audio_repository, id_service, file_store_service)


def test_storage_coordinator_instantiation(audio_storage_coordinator):
    assert audio_storage_coordinator is not None


def test_storage_coordinator_store_no_data(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'extension': 'mp4'}

    audio_storage_coordinator.store(audio_dict)

    assert len(audio_storage_coordinator.audio_repository.items) == 0


def test_storage_coordinator_store_data(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': 'BASE64_DATA',
        'extension': 'mp4'}

    audio_storage_coordinator.store(audio_dict)

    assert len(audio_storage_coordinator.audio_repository.items) == 1


def test_storage_coordinator_store_file(audio_storage_coordinator):
    audio_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': ('"iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42'
                 'mNk+H+1noEIwDiqkL4KAUP4F0koL9m+AAAAAElFTkSuQmCC",'),
        'extension': 'png'}

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
        iter(audio_storage_coordinator.audio_repository.items.values()))
    assert audio.uri == audio.id
