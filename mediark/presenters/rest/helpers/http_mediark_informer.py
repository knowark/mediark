from typing import List, Any
from ....application.domain.common import TenantProvider
from ....application.informers import (
    StandardMediarkInformer, MediaDictList, SearchDomain)


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
            item['url'] = download_url + '/' + uri
        return items

    async def search_media(self, domain: SearchDomain) -> MediaDictList:
        result = await super().search_media(domain)
        media_download = f"{self.domain}/download"
        return self._prepend_download(media_download, result)
