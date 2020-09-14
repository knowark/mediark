import os
from pathlib import Path
from pytest import fixture
from base64 import b64encode
from mediark.core.suppliers import (
    DirectoryArranger, DirectoryFileStoreService)
from mediark.core import config
from mediark.application.domain.common import StandardTenantProvider, Tenant


@fixture(scope='session')
def directory_arranger(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('media')
    base_path = str(tmpdir.mkdir('images'))
    directory_arranger = DirectoryArranger(base_path)
    directory_arranger.matrix_dimensions = list('abc')
    return directory_arranger


@fixture
def encoded_image() -> bytes:
    filename = os.path.join(
        os.path.dirname(__file__), "assets/SampleImage.png")
    with open(filename, "rb") as f:
        binary_data = f.read()
    return b64encode(binary_data)


@fixture
def directory_file_store_service(tmp_path):
    config['dir_path'] = tmp_path / 'data'
    standard_tenant_provider = StandardTenantProvider()
    standard_tenant_provider.setup(Tenant(id='2', name="custom-tenant"))
    return DirectoryFileStoreService(
        standard_tenant_provider, config)
