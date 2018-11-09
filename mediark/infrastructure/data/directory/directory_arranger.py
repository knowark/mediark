from pathlib import Path
from typing import Union, Tuple
from base64 import decodebytes


class DirectoryArranger:
    def __init__(self, base_path: str, extension: str) -> None:
        self.base_path = base_path
        self.extension = extension
        self.matrix_dimensions = list('0123456789abcdef')

    def setup(self):
        self._create_sub_directories(self.base_path)
        root_dirs = [x for x in Path(self.base_path).iterdir()
                     if x.is_dir()]
        for subdir in root_dirs:
            self._create_sub_directories(str(subdir))

    def _create_sub_directories(self, root_path: str) -> None:
        base_dir = Path(root_path)
        for i in self.matrix_dimensions:
            for j in self.matrix_dimensions:
                sub_dir = base_dir.joinpath(i + j)
                sub_dir.mkdir(parents=True, exist_ok=True)

    def _get_subdirs(self, id: str) -> Tuple[str, str]:
        if len(id) < 4:
            raise ValueError("Invalid UUIDv4. Too short.")
        first_dir = id[:2]
        second_dir = id[2:4]
        return first_dir, second_dir
