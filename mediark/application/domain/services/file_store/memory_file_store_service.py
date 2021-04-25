from collections import defaultdict
from typing import Dict, List, Tuple, Any
from ...common import TenantProvider
from .file_store_service import FileStoreService, Reader, Writer


class MemoryFileStoreService(FileStoreService):
    def __init__(self, tenant_service: TenantProvider) -> None:
        self.files: Dict[str, Dict[str, bytes]] = defaultdict(dict)
        self.tenant_service = tenant_service

    async def submit(self, contexts: List[Dict[str, Any]]) -> List[str]:
        uris = []
        for context in contexts:
            uri = context['id']
            stream = context['stream']
            if not stream:
                uris.append('')
                continue
            content = await stream.read(-1)
            self.files[self._location][uri] = content
            uris.append(uri)
        return uris

    async def load(self, uri: str, stream: Writer) -> None:
        content = self.files[self._location][uri]
        await stream.write(content)

    @property
    def _location(self) -> str:
        return self.tenant_service.tenant.zone or 'default'
