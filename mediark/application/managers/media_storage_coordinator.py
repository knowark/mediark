from ..models import Media
from typing import List, Tuple, Dict, Any
from base64 import b64decode
from ..repositories import MediaRepository
from ..services import IdService, FileStoreService
from ..utilities import EntityNotFoundError
from .types import RecordList


class MediaStorageCoordinator:
    def __init__(self,
                 media_repository: MediaRepository,
                 id_service: IdService,
                 file_store_service: FileStoreService) -> None:
        self.media_repository = media_repository
        self.id_service = id_service
        self.file_store_service = file_store_service

    async def store(self, media_records: RecordList) -> None:
        contents = self._extract_contents(media_records)
        medias = await self.media_repository.add(
            [Media(**media_dict) for media_dict in media_records])

        contexts = [{'content': content, **vars(media)}
                    for media, content in zip(medias, contents)]

        uris = await self.file_store_service.store(contexts)
        for media, uri in zip(medias, uris):
            media.uri = uri

        await self.media_repository.add(medias)

    def _extract_contents(self, media_records: RecordList) -> List[bytes]:
        contents: List[bytes] = []
        for media_dict in media_records:
            content = media_dict.pop('data', None)
            if not content:
                raise ValueError("All the medias must have content.")
            contents.append(b64decode(content))
        return contents
