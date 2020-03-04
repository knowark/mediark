import time
from pathlib import Path
from typing import Tuple, Dict, Union
from base64 import b64decode
from uuid import UUID
from .....application.utilities import TenantProvider
from .....application.services import FileStoreService
from ....core import HttpClientSupplier
from .swift_auth_supplier import SwiftAuthSupplier


class SwiftFileStoreService(FileStoreService):
    def __init__(
            self, tenant_service: TenantProvider,
            auth_supplier: SwiftAuthSupplier,
            client: HttpClientSupplier,
            data_config: dict) -> None:
        self.tenant_service = tenant_service
        self.auth_supplier = auth_supplier
        self.client = client
        self.data_config = data_config

    async def store(self, content: bytes,
                    context: Dict[str, str]) -> str:

        token = await self.auth_supplier.authenticate()
        object_name = self._make_object_name(context)
        url = self._make_url(object_name)

        await self._upload_object(token, url, content)

        return object_name

    def _make_object_name(self, context: Dict[str, str]) -> str:
        object_type = context.get('type', 'general')
        timestamp = int(context.get('timestamp', time.time()))
        year_month = time.strftime('%Y%m', time.gmtime(timestamp))
        extension = context.get("extension", "txt")
        object_id = context["id"]

        return f'{object_type}/{year_month}/{object_id}.{extension}'

    def _make_url(self, object_name: str) -> str:
        config = self.data_config['cloud']['swift']
        object_store_url = config['object_store_url']
        container_list = []
        prefix = config.get('container_prefix')
        if prefix:
            container_list.append(prefix)
        container_list.append(self.tenant_service.tenant.slug)
        suffix = config.get('container_suffix')
        if suffix:
            container_list.append(suffix)
        container = "-".join(container_list)

        return f'{object_store_url}/{container}/{object_name}'

    async def _upload_object(
            self, token: str, url: str, content: bytes) -> None:
        headers = {'X-Auth-Token': token}
        async with self.client.put(
                url, headers=headers, data=content) as response:
            pass
