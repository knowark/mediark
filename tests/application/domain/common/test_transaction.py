from pytest import fixture
from mediark.application.domain.common import (
    TransactionManager, MemoryTransactionManager)


@fixture
def transation_manager() -> MemoryTransactionManager:
    return MemoryTransactionManager()


def test_transaction_manager_creation(transation_manager):
    assert isinstance(transation_manager, TransactionManager)


def test_transaction_manager_methods() -> None:
    methods = TransactionManager.__abstractmethods__  # type: ignore
    assert '__call__' in methods


def test_transaction_manager_call(transation_manager):
    class DummyClass:
        pass

    result = transation_manager(DummyClass)

    assert result == DummyClass
