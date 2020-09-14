from typing import List, Any
from ....application.domain.common import TenantProvider
from ....application.informers import (
    StandardMediarkInformer, MediaDictList)
from ....application.informers.types import QueryDomain
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
            item['url'] = download_url + '/' + uri
        return items

    async def search_media(self, domain: QueryDomain) -> MediaDictList:
        result = await super().search_media(Media, domain)
        media_download = f"{self.domain}/download"
        return self._prepend_download(media_download, result)
