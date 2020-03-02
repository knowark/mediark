from pathlib import Path
from typing import Tuple
from base64 import b64decode
from uuid import UUID
from ....application.utilities import TenantProvider
from ....application.services import FileStoreService


class DirectoryFileStoreService(FileStoreService):
    def __init__(
        self, tenant_service: TenantProvider, data_config: dict,
        data_type: str, extension: str = None
    ) -> None:

        self.tenant_service = tenant_service
        self.data_config = data_config
        self.data_type = data_type
        self.extension = extension or \
            self.data_config["media"][self.data_type]["extension"]

    async def store(
            self, file_id: str, content: str, extension: str = None) -> str:
        first_dir, second_dir = self._get_subdirs(file_id)
        extension = extension or self.extension
        binary_data = b64decode(content)

        base_path = Path("{0}/{1}/{2}/{3}".format(
            self.data_config["dir_path"],
            self.tenant_service.tenant.slug,
            self.data_config["media"]["dir_path"],
            self.data_config["media"][self.data_type]["dir_path"]))

        base_path.mkdir(parents=True, exist_ok=True)

        uri = "{0}/{1}/{2}.{3}".format(
            first_dir, second_dir, file_id, extension)
        file_path = Path(base_path).joinpath(uri)
        file_path.absolute().parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("wb") as f:
            f.write(binary_data)
        return uri

    def _get_subdirs(self, file_id: str) -> Tuple[str, str]:
        UUID(hex=file_id, version=4)
        first_dir = file_id[:2]
        second_dir = file_id[2:4]
        return first_dir, second_dir
