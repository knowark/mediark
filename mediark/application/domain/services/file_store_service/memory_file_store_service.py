import uuid
from abc import ABC, abstractmethod
from base64 import b64decode
from collections import defaultdict
from typing import Dict, List, Tuple, Union, Any, cast
from ...common import TenantProvider, AuthProvider
from .file_store_service import FileStoreService


class MemoryFileStoreService(FileStoreService):
    def __init__(self, tenant_service: TenantProvider,
                 auth_provider: AuthProvider) -> None:
        self.files: Dict[str, Dict[str, bytes]] = defaultdict(dict)
        self.tenant_service = tenant_service

    async def store(self, contexts: List[Dict[str, Any]]) -> List[str]:
        file_ids = []
        for context in contexts:
            file_id = context['id']
            content: bytes = context.pop('content')
            self.files[self._location][file_id] = content
            file_ids.append(file_id)
        return file_ids

    async def load(self, uri: str) -> Tuple[bytes, Dict[str, Any]]:
        content = b''
        context: Dict[str, Any] = {}
        return content, context

    @property
    def _location(self) -> str:
        return self.tenant_service.tenant.zone or 'default'
