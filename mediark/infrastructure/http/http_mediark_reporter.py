from typing import List, Any
from ...application.reporters import (
    StandardMediarkReporter, ImageDictList, AudioDictList, SearchDomain)


class HttpMediarkReporter(StandardMediarkReporter):

    def __init__(self, image_download: str,
                 audio_download: str, *args) -> None:
        super().__init__(*args)
        self.image_download = image_download
        self.audio_download = audio_download

    @staticmethod
    def _prepend_download(download_url: str, items: List[Any]) -> List[Any]:
        for item in items:
            uri = item.pop('uri')
            item['url'] = download_url + '/' + uri
        return items

    def search_images(self, domain: SearchDomain) -> ImageDictList:
        result = super().search_images(domain)
        return self._prepend_download(self.image_download, result)

    def search_audios(self, domain: SearchDomain) -> AudioDictList:
        result = super().search_audios(domain)
        return self._prepend_download(self.audio_download, result)
