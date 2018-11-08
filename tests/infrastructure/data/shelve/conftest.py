import shelve
from pytest import fixture


@fixture(scope='session')
def dummy_shelve(tmpdir_factory):
    filename = str(tmpdir_factory.mktemp('data').join('dummy.db'))
    return filename
