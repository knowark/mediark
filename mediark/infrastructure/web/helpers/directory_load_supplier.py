from typing import Any
from pathlib import Path


class DirectoryLoadSupplier ():
    def __init__(self, data_path: str, media_dir: str):
        self.data_path = data_path
        self.media_dir = media_dir

    def file_path(self, tenant: str, type: str, uri: str) -> Path:
        return Path(self.data_path).joinpath(
            f"{tenant}/{self.media_dir}/{type}/{uri}")
