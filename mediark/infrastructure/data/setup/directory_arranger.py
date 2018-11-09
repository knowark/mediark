from pathlib import Path
from typing import Union, Tuple, List
from base64 import decodebytes


class DirectoryArranger:
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path
        self.matrix_dimensions = list('0123456789abcdef')

    @staticmethod
    def make_directory(path: str) -> None:
        Path(path).mkdir(parents=True, exist_ok=True)

    def setup(self) -> None:
        self.make_directory(self.base_path)
        self._create_sub_directories(self.base_path)
        root_dirs = [x for x in Path(self.base_path).iterdir() if x.is_dir()]
        for subdir in root_dirs:
            self._create_sub_directories(str(subdir))

    def _create_sub_directories(self, root_path: str) -> None:
        base_dir = Path(root_path)
        for i in self.matrix_dimensions:
            for j in self.matrix_dimensions:
                sub_dir = base_dir.joinpath(i + j)
                sub_dir.mkdir(parents=True, exist_ok=True)
