from pathlib import Path
from typing import Tuple
from base64 import b64decode
from ....application.services import FileStoreService


class DirectoryFileStoreService(FileStoreService):
    def __init__(self, base_path: str, extension: str) -> None:
        self.base_path = base_path
        self.extension = extension

    def store(self, locator: str, content: str, extension: str = None) -> str:
        first_dir, second_dir = self._get_subdirs(locator)
        extension = extension or self.extension
        binary_data = b64decode(content)

        uri = "{0}/{1}/{2}.{3}".format(
            first_dir, second_dir, locator, extension)

        file_path = Path(self.base_path).joinpath(uri)
        with file_path.open("wb") as f:
            f.write(binary_data)

        return uri

    def _get_subdirs(self, locator: str) -> Tuple[str, str]:
        if len(locator) < 4:
            raise ValueError("Invalid UUIDv4. Too short.")
        first_dir = locator[:2]
        second_dir = locator[2:4]
        return first_dir, second_dir
