from collections import defaultdict
from typing import Dict, List, Tuple, Any
from ...common import TenantProvider, AuthProvider
from .file_store_service import FileStoreService, Reader, Writer


class MemoryFileStoreService(FileStoreService):
    def __init__(self, tenant_service: TenantProvider,
                 auth_provider: AuthProvider) -> None:
        self.files: Dict[str, Dict[str, bytes]] = defaultdict(dict)
        self.tenant_service = tenant_service
        self.content = b''

    async def store(self, contexts: List[Dict[str, Any]]) -> List[str]:
        file_ids = []
        for context in contexts:
            file_id = context['id']
            content: bytes = context.pop('content')
            self.files[self._location][file_id] = content
            file_ids.append(file_id)
        return file_ids

    async def load(self, uri: str, stream: Writer) -> Dict[str, Any]:
        context: Dict[str, Any] = {}
        await stream.write(self.content)
        return context

    async def submit(self, contexts: List[Dict[str, Any]]) -> List[str]:
        file_ids = []
        for context in contexts:
            file_id = context['id']
            stream = context['stream']
            content = await stream.read(-1)
            self.files[self._location][file_id] = content
            file_ids.append(file_id)
        return file_ids

    @property
    def _location(self) -> str:
        return self.tenant_service.tenant.zone or 'default'
