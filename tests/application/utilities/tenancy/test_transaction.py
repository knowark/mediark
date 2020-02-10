from pytest import fixture
from mediark.application.utilities import MemoryTransactionManager


@fixture
def dummy_class():
    class DummyClass:
        def sum(self, value1: int, value2: int) -> int:
            return value1 + value2

    return DummyClass


def test_memory_transaction_manager(dummy_class) -> None:
    result1 = dummy_class().sum(1, 1)
    result2 = MemoryTransactionManager()(dummy_class)().sum(1, 1)

    assert result1 == result2
