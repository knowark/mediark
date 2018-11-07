from pytest import fixture
from mediark.application.repositories import (
    MemoryImageRepository, ExpressionParser)
from mediark.application.services import StandardIdService
from mediark.application.coordinators import ImageStorageCoordinator


@fixture
def image_storage_coordinator():
    parser = ExpressionParser()
    image_repository = MemoryImageRepository(parser)
    id_service = StandardIdService()

    return ImageStorageCoordinator(
        image_repository, id_service)


def test_storage_coordinator_instantiation(image_storage_coordinator):
    assert image_storage_coordinator is not None


def test_storage_coordinator_store(image_storage_coordinator):
    image_dict = {
        'namespace': 'https://example.com',
        'reference': '00648c29-eca2-4112-8a1a-4deedb443188',
        'extension': 'jpg'}

    image_storage_coordinator.store(image_dict)

    assert len(image_storage_coordinator.image_repository.items) == 1
