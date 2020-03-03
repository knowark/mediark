from pathlib import Path
from typing import Tuple
from base64 import b64decode
from uuid import UUID
from .....application.utilities import TenantProvider
from .....application.services import FileStoreService


class SwiftFileStoreService(FileStoreService):
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
        return file_id
