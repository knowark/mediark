from pathlib import Path
from pytest import fixture, raises
from mediark.infrastructure.data import DirectoryArranger


def test_directory_arranger_instantiation(directory_arranger):
    assert isinstance(directory_arranger, DirectoryArranger)


def test_directory_arranger_create_directory_structure(
        directory_arranger):

    directory_arranger.setup()

    base_dir = Path(directory_arranger.base_path)
    subdirs = [str(x) for x in base_dir.iterdir() if x.is_dir()]
    matrix_dimensions = directory_arranger.matrix_dimensions

    for i in matrix_dimensions:
        for j in matrix_dimensions:
            sub_dir = str(base_dir.joinpath(i + j))
            assert sub_dir in subdirs


def test_directory_arranger_create_nested_directory_structure(
        directory_arranger):

    directory_arranger.setup()

    base_dir = Path(directory_arranger.base_path)
    matrix_dimensions = directory_arranger.matrix_dimensions
    root_dirs = [x for x in base_dir.iterdir() if x.is_dir()]

    for root_sub_dir in root_dirs:
        subdirs = [str(x) for x in root_sub_dir.iterdir() if x.is_dir()]
        for i in matrix_dimensions:
            for j in matrix_dimensions:
                sub_dir = str(root_sub_dir.joinpath(i + j))
                assert sub_dir in subdirs
