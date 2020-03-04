from pathlib import Path
from typing import Tuple, Dict
from base64 import b64decode
from uuid import UUID
from .....application.utilities import TenantProvider
from .....application.services import FileStoreService
from .swift_auth_supplier import SwiftAuthSupplier


class SwiftFileStoreService(FileStoreService):
    def __init__(
        self, tenant_service: TenantProvider,
        auth_supplire: SwiftAuthSupplier,
        data_config: dict
    ) -> None:

        self.tenant_service = tenant_service
        self.data_config = data_config

    async def store(self, content: str, context: Dict[str, str]) -> str:
        return ''
