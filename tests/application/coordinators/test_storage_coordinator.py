from pytest import fixture
from mediark.application.coordinators import StorageCoordinator


@fixture
def storage_coordinator():
    storage_coordinator = StorageCoordinator()
    return storage_coordinator


def test_storage_coordinator_instantiation(storage_coordinator):
    assert storage_coordinator is not None
