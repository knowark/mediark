from ..domain.models import Media
from typing import List
from base64 import b64decode
from ..domain.repositories import MediaRepository
from ..domain.services import IdService, FileStoreService
from ..domain.common import RecordList


class MediaStorageManager:
    def __init__(self,
                 media_repository: MediaRepository,
                 id_service: IdService,
                 file_store_service: FileStoreService) -> None:
        self.media_repository = media_repository
        self.id_service = id_service
        self.file_store_service = file_store_service

    async def submit(self, submission_records: RecordList) -> None:
        medias = await self.media_repository.add(
            [Media(**record['media']) for record in submission_records])
        streams = [record.get('stream') for record in submission_records]

        contexts = [{'stream': stream, **vars(media)}
                    for media, stream in zip(medias, streams)]

        uris = await self.file_store_service.submit(contexts)
        for media, uri in zip(medias, uris):
            media.uri = uri

        await self.media_repository.add(medias)
