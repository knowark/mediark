import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict
from ...utilities import TenantProvider, AuthProvider
from .file_store_service import FileStoreService


class MemoryFileStoreService(FileStoreService):
    def __init__(self, tenant_service: TenantProvider,
                 auth_provider: AuthProvider) -> None:
        self.files: Dict[str, Dict[str, str]] = defaultdict(dict)
        self.tenant_service = tenant_service

    async def store(
            self, file_id: str, content: str, extension: str = None) -> str:
        self.files[self._location][file_id] = content
        return file_id

    @property
    def _location(self) -> str:
        return self.tenant_service.tenant.zone or 'default'
