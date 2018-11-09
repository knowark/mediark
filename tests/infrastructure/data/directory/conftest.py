import os
from pathlib import Path
from pytest import fixture
from base64 import b64encode
from mediark.infrastructure.data import (
    DirectoryArranger, DirectoryFileStoreService)


@fixture(scope='session')
def directory_arranger(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('media')
    base_path = str(tmpdir.mkdir('images'))
    directory_arranger = DirectoryArranger(base_path)
    directory_arranger.matrix_dimensions = list('abc')
    return directory_arranger


@fixture
def base64_image() -> bytes:
    filename = os.path.join(
        os.path.dirname(__file__), "assets/locked-padlock.png")
    with open(filename, "rb") as f:
        binary_data = f.read()
    return b64encode(binary_data)


@fixture(scope='session')
def directory_file_store_service(tmpdir_factory, directory_arranger):
    directory_arranger.setup()
    base_path = directory_arranger.base_path
    extension = 'png'

    filestore_manager = DirectoryFileStoreService(base_path, extension)
    return filestore_manager
