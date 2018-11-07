from pytest import fixture
from mediark.application.coordinators import ImageStorageCoordinator


@fixture
def image_storage_coordinator():
    image_storage_coordinator = ImageStorageCoordinator()
    return image_storage_coordinator


def test_storage_coordinator_instantiation(image_storage_coordinator):
    assert image_storage_coordinator is not None
