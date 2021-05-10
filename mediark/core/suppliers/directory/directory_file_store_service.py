import time
import aiofiles
import aiofiles.os
from pathlib import Path
from typing import List, Dict, Any
from base64 import b64decode
from uuid import UUID
from ....application.domain.common import TenantProvider
from ....application.domain.services import FileStoreService, Reader, Writer


class DirectoryFileStoreService(FileStoreService):
    def __init__(self, tenant_service: TenantProvider,
                 data_config: dict) -> None:
        self.tenant_service = tenant_service
        self.data_config = data_config
        self.chunk_size = 512 * 1024

    async def submit(self, contexts: List[Dict[str, Any]]) -> List[str]:
        uris = []
        for context in contexts:
            stream: Reader = context.pop('stream')
            uri = self._make_object_name(context)
            file_path = self._make_file_path(uri)
            file_path.absolute().parent.mkdir(parents=True, exist_ok=True)

            generator = self._generate_chunked_data(stream)
            async with aiofiles.open(str(file_path), 'wb') as f:
                async for chunk in generator:
                    await f.write(chunk)

            uris.append(uri)

        return uris

    async def load(self, uri: str, stream: Writer) -> None:
        file_path = self._make_file_path(uri)
        async with aiofiles.open(str(file_path), 'rb') as f:
            generator = self._generate_chunked_data(f)
            async for chunk in generator:
                await stream.write(chunk)

    async def delete(self, uri: str) -> None:
        file_path = self._make_file_path(uri)
        await aiofiles.os.remove(str(file_path))

    async def _generate_chunked_data(self, stream: Reader) -> None:
        chunk = await stream.read(self.chunk_size)
        while chunk:
            yield chunk
            chunk = await stream.read(self.chunk_size)

    def _make_file_path(self, uri: str) -> Path:
        base_path = Path("{0}/{1}/{2}".format(
            self.data_config["dir_path"],
            self.tenant_service.tenant.slug,
            self.data_config["media"]["dir_path"]))

        return Path(base_path).joinpath(uri)

    def _make_object_name(self, context: Dict[str, str]) -> str:
        object_type = context.get('type', '')
        timestamp = int(context.get('timestamp', context['created_at']))
        year_month_day = time.strftime('%Y/%m/%d', time.gmtime(timestamp))
        object_id = context["id"]
        extension = Path(context['name']).suffix
        return f'{object_type}/{year_month_day}/{object_id}{extension}'
