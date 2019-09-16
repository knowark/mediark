from pathlib import Path
from typing import Tuple
from base64 import b64decode
from pathlib import Path
from mediark.application.utilities import TenantProvider
from ....application.services import FileStoreService


class DirectoryFileStoreService(FileStoreService):
    def __init__(
        self, tenant_service: TenantProvider, data_config: dict,
        data_type: str
    ) -> None:

        base_path = Path("{0}/{1}/{2}/{3}".format(
            data_config["dir_path"], tenant_service.tenant.slug,
            data_config["media"]["dir_path"],
            data_config["media"][data_type]["dir_path"]))

        base_path.mkdir(parents=True, exist_ok=True)

        self.base_path = str(base_path)
        self.extension = data_config["media"][data_type]["extension"]

    def store(self, file_id: str, content: str, extension: str = None) -> str:
        first_dir, second_dir = self._get_subdirs(file_id)
        extension = extension or self.extension
        binary_data = b64decode(content)

        uri = "{0}/{1}/{2}.{3}".format(
            first_dir, second_dir, file_id, extension)
        file_path = Path(self.base_path).joinpath(uri)
        file_path.absolute().parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("wb") as f:
            f.write(binary_data)
        return uri

    def _get_subdirs(self, file_id: str) -> Tuple[str, str]:
        if len(file_id) < 4:
            raise ValueError("Invalid UUIDv4. Too short.")
        first_dir = file_id[:2]
        second_dir = file_id[2:4]
        return first_dir, second_dir
