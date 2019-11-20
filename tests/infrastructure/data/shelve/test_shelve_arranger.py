from pathlib import Path
from pytest import fixture, raises
from mediark.infrastructure.data import ShelveArranger


def test_directory_arranger(tmp_path):
    tmpdir = tmp_path / Path('media')
    tmpdir.mkdir()
    tmpdir = tmpdir / Path("images")
    tmpdir.mkdir()
    shelve_arranger = ShelveArranger()
    shelve_arranger.make_shelve(str(tmpdir / 'images.db'))
    assert isinstance(shelve_arranger, ShelveArranger)
