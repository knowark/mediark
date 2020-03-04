from pathlib import Path
from typing import Tuple, Dict, Union
from base64 import b64decode
from uuid import UUID
from .....application.utilities import TenantProvider
from .....application.services import FileStoreService
from .swift_auth_supplier import SwiftAuthSupplier


class SwiftFileStoreService(FileStoreService):
    def __init__(
            self, tenant_service: TenantProvider,
            auth_supplier: SwiftAuthSupplier,
            data_config: dict) -> None:
        self.tenant_service = tenant_service
        self.auth_supplier = auth_supplier
        self.data_config = data_config

    async def store(self, content: Union[str, bytes],
                    context: Dict[str, str]) -> str:
        if not isinstance(content, bytes):
            content = b64decode(content)

        token = await self.auth_supplier.authenticate()

        print('Token:::', token)

        return 'the_uri_1234'
