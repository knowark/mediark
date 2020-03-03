from typing import List, Any
from ....application.utilities import TenantProvider
from ....application.reporters import (
    StandardMediarkReporter, ImageDictList, AudioDictList, SearchDomain)


class HttpMediarkReporter(StandardMediarkReporter):

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

    async def search_images(self, domain: SearchDomain) -> ImageDictList:
        result = await super().search_images(domain)
        tenant = self.tenant_provider.tenant.slug
        image_download = f"{self.domain}/download/{tenant}/images"
        return self._prepend_download(image_download, result)

    async def search_audios(self, domain: SearchDomain) -> AudioDictList:
        result = await super().search_audios(domain)
        tenant = self.tenant_provider.tenant.slug
        audio_download = f"{self.domain}/download/{tenant}/audios"
        return self._prepend_download(audio_download, result)
