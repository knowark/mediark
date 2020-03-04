import uuid
from abc import ABC, abstractmethod
from base64 import b64decode
from collections import defaultdict
from typing import Dict, Union
from ...utilities import TenantProvider, AuthProvider
from .file_store_service import FileStoreService


class MemoryFileStoreService(FileStoreService):
    def __init__(self, tenant_service: TenantProvider,
                 auth_provider: AuthProvider) -> None:
        self.files: Dict[str, Dict[str, bytes]] = defaultdict(dict)
        self.tenant_service = tenant_service

    async def store(self, content: bytes,
                    context: Dict[str, str]) -> str:
        file_id = context['id']
        self.files[self._location][file_id] = content
        return file_id

    @property
    def _location(self) -> str:
        return self.tenant_service.tenant.zone or 'default'
