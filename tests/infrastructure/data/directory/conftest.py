from pytest import fixture
from mediark.infrastructure.data import DirectoryArranger


@fixture(scope='session')
def directory_arranger(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('media')
    base_path = str(tmpdir.mkdir('images'))
    extension = 'png'
    directory_arranger = DirectoryArranger(base_path, extension)
    directory_arranger.matrix_dimensions = list('abc')
    return directory_arranger
