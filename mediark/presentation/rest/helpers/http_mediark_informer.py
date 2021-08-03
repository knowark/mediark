from typing import List, Any
from ....application.domain.common import TenantProvider
from ....application.operation.informers import StandardMediarkInformer
from ....application.domain.common import QueryDomain, RecordList
from ....application.domain.models import Media


class HttpMediarkInformer(StandardMediarkInformer):

    def __init__(self, domain: str, tenant_provider: TenantProvider,
                 *args) -> None:
        super().__init__(*args)
        self.domain = domain
        self.tenant_provider = tenant_provider

    @staticmethod
    def _prepend_download(download_url: str, items: List[Any]) -> List[Any]:
        for item in items:
            uri = item.pop('uri')
            path = item.get('path') or uri
            item['url'] = f"{download_url}/{path}"
        return items

    async def search(self,
                     model: str,
                     domain: QueryDomain = None,
                     limit: int = 1000,
                     offset: int = 0) -> RecordList:
        result = await super().search('media', domain)
        tenant = self.tenant_provider.tenant
        media_download = f"{self.domain}/download/{tenant.slug}"
        return self._prepend_download(media_download, result)
