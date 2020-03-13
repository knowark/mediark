import time
import io
import tarfile
from aiohttp import ClientResponse
from pathlib import Path
from typing import List, Tuple, Dict, Union, Any
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

    async def store(self, contexts: List[Dict[str, Any]]) -> List[str]:
        uri_content_pairs: List[Tuple[str, bytes]] = []
        for context in contexts:
            content: bytes = context.pop('content')
            uri = self._make_object_name(context)
            uri_content_pairs.append((uri, content))

        url = self._make_url()
        archive_content = self._tar_contents(uri_content_pairs)
        if not archive_content:
            raise ValueError(f'Not archive content: <{archive_content}>')

        token = await self.auth_supplier.authenticate()
        await self._upload_object(token, url, archive_content)

        return [pair[0] for pair in uri_content_pairs]

    async def load(self, uri: str) -> Tuple[bytes, Dict[str, Any]]:
        token = await self.auth_supplier.authenticate()
        url = self._make_url(uri)
        return await self._download_object(token, url)

    def _make_object_name(self, context: Dict[str, str]) -> str:
        object_type = context.get('type', 'general')
        timestamp = int(context.get('timestamp', context['created_at']))
        year_month_day = time.strftime('%Y/%m/%d', time.gmtime(timestamp))
        extension = context.get("extension", "txt")
        object_id = context["id"]

        return f'{object_type}/{year_month_day}/{object_id}.{extension}'

    def _make_url(self, object_name: str = "") -> str:
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

        url = f'{object_store_url}/{container}'
        if object_name:
            url = f'{url}/{object_name}'

        return url

    def _tar_contents(
            self, uri_content_pairs: List[Tuple[str, bytes]]) -> bytes:
        archive = io.BytesIO()
        with tarfile.open(fileobj=archive, mode='w:gz') as tar:
            for uri, content in uri_content_pairs:
                tarinfo = tarfile.TarInfo(uri)
                tarinfo.size = len(content)
                fileobj = io.BytesIO(content)
                tar.addfile(tarinfo, fileobj)

        return archive.getvalue()

    async def _upload_object(
            self, token: str, url: str, content: bytes) -> None:
        headers = {'X-Auth-Token': token}
        url = f'{url}?extract-archive=tar.gz'
        async with self.client.put(
                url, headers=headers, data=content) as response:
            body = await response.read()

    async def _download_object(
            self, token: str, url: str) -> Tuple[bytes, Dict[str, Any]]:
        headers = {'X-Auth-Token': token}
        async with self.client.get(url, headers=headers) as response:
            return (await response.read(), {
                'status': response.status,
                'headers': response.headers,
            })
