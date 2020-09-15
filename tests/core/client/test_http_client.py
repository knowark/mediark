from mediark.core.client import HttpClientSupplier
from pytest import fixture, raises


def test_http_client():
    with raises(RecursionError):
        hpc = HttpClientSupplier()
        hpc.client = 10
        hpc.__getattribute__
