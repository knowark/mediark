from pytest import fixture


@fixture(scope='session')
def media_directory(tmpdir_factory):
    directory = str(tmpdir_factory.mktemp('media'))
    return directory


@fixture(scope='session')
def filestore_manager_image(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('data')
    base_path = str(tmpdir.mkdir('static'))
    extension = 'png'
    filestore_manager = FilestoreManager(base_path, extension)
    return filestore_manager
