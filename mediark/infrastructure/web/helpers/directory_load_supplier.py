from typing import Any
from pathlib import Path
from flask import send_from_directory


class DirectoryLoadSupplier ():
    def __init__(self, data_path: str, media_dir: str):
        self.data_path = data_path
        self.media_dir = media_dir

    def send_file(self, tenant: str, type: str, uri: str) -> Any:
        directory = Path(self.data_path).joinpath(
            tenant+"/"+self.media_dir+"/"+type+"/")
        return send_from_directory(directory, uri)
