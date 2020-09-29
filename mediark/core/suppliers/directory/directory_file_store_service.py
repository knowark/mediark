import time
from pathlib import Path
from typing import List, Dict, Any
from base64 import b64decode
from uuid import UUID
from ....application.domain.common import TenantProvider
from ....application.domain.services import FileStoreService


class DirectoryFileStoreService(FileStoreService):
    def __init__(self, tenant_service: TenantProvider,
                 data_config: dict) -> None:
        self.tenant_service = tenant_service
        self.data_config = data_config

    async def store(self, contexts: List[Dict[str, Any]]) -> List[str]:
        uris = []
        for context in contexts:
            content: bytes = context.pop('content')
            binary_data = b64decode(content)
            uri = self._make_object_name(context)
            file_path = self._make_file_path(uri)

            file_path.absolute().parent.mkdir(parents=True, exist_ok=True)

            with file_path.open("wb") as f:
                f.write(binary_data)

            uris.append(uri)

        return uris

    async def load(self, uri: str) -> Any:
        file_path = self._make_file_path(uri)
        with file_path.open('rb') as f:
            return f.read(), {
                'status': 200,
                'headers': {}
            }

    def _make_file_path(self, uri: str) -> Path:
        base_path = Path("{0}/{1}/{2}".format(
            self.data_config["dir_path"],
            self.tenant_service.tenant.slug,
            self.data_config["media"]["dir_path"]))

        return Path(base_path).joinpath(uri)

    def _make_object_name(self, context: Dict[str, str]) -> str:
        object_type = context.get('type', 'general')
        timestamp = int(context.get('timestamp', context['created_at']))
        year_month_day = time.strftime('%Y/%m/%d', time.gmtime(timestamp))
        extension = context.get("extension", "txt")
        object_id = context["id"]

        return f'{object_type}/{year_month_day}/{object_id}.{extension}'
