from pathlib import Path
from typing import Tuple, Dict, Any
from base64 import b64decode
from uuid import UUID
from ....application.utilities import TenantProvider
from ....application.services import FileStoreService


class DirectoryFileStoreService(FileStoreService):
    def __init__(self, tenant_service: TenantProvider,
                 data_config: dict) -> None:

        self.tenant_service = tenant_service
        self.data_config = data_config

    async def store(self, content: bytes, context: Dict[str, str]) -> str:
        file_id = context['id']
        data_type = context['type']
        extension = context.get('extension', 'txt')
        first_dir, second_dir = self._get_subdirs(file_id)
        binary_data = b64decode(content)

        base_path = Path("{0}/{1}/{2}/{3}".format(
            self.data_config["dir_path"],
            self.tenant_service.tenant.slug,
            self.data_config["media"]["dir_path"],
            self.data_config["media"][data_type]["dir_path"]))

        base_path.mkdir(parents=True, exist_ok=True)

        uri = "{0}/{1}/{2}.{3}".format(
            first_dir, second_dir, file_id, extension)
        file_path = Path(base_path).joinpath(uri)
        file_path.absolute().parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("wb") as f:
            f.write(binary_data)
        return uri

    async def load(self, uri: str) -> Any:
        pass

    def _get_subdirs(self, file_id: str) -> Tuple[str, str]:
        UUID(hex=file_id, version=4)
        first_dir = file_id[:2]
        second_dir = file_id[2:4]
        return first_dir, second_dir
