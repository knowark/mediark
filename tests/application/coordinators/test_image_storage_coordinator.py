from pytest import fixture
from mediark.application.repositories import (
    MemoryImageRepository, ExpressionParser)
from mediark.application.services import (
    StandardIdService, MemoryFileStoreService)
from mediark.application.coordinators import ImageStorageCoordinator


@fixture
def image_storage_coordinator():
    parser = ExpressionParser()
    image_repository = MemoryImageRepository(parser)
    id_service = StandardIdService()
    file_store_service = MemoryFileStoreService()

    return ImageStorageCoordinator(
        image_repository, id_service, file_store_service)


def test_storage_coordinator_instantiation(image_storage_coordinator):
    assert image_storage_coordinator is not None


def test_storage_coordinator_store_no_data(image_storage_coordinator):
    image_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'extension': 'jpg'}

    image_storage_coordinator.store(image_dict)

    assert len(image_storage_coordinator.image_repository.items) == 0


def test_storage_coordinator_store_data(image_storage_coordinator):
    image_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'data': 'BASE64_DATA',
        'extension': 'jpg'}

    image_storage_coordinator.store(image_dict)

    assert len(image_storage_coordinator.image_repository.items) == 1


def test_storage_coordinator_store_file(image_storage_coordinator):
    image_dict = {
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

    image_storage_coordinator.file_store_service = MockFileStoreService()
    image_storage_coordinator.store(image_dict)

    assert called is True
    image = next(
        iter(image_storage_coordinator.image_repository.items.values()))
    assert image.uri == image.id
