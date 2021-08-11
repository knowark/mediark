from typing import List
from base64 import b64decode
from validark import validate
from ...domain.models import Media
from ...domain.services.repositories import MediaRepository
from ...domain.services import IdService, FileStoreService
from ...domain.common import RecordList
from .common import submission_schema


class MediaStorageManager:
    def __init__(self,
                 media_repository: MediaRepository,
                 id_service: IdService,
                 file_store_service: FileStoreService) -> None:
        self.media_repository = media_repository
        self.id_service = id_service
        self.file_store_service = file_store_service

    async def submit(self, submission_records: RecordList) -> None:
        records = validate(submission_schema, submission_records)
        medias = await self.media_repository.add(
            [Media(**record['media']) for record in records])
        streams = [record.get('stream') for record in records]

        contexts = [{'stream': stream, **vars(media)}
                    for media, stream in zip(medias, streams)]

        uris = await self.file_store_service.submit(contexts)
        for media, uri in zip(medias, uris):
            if uri:
                media.uri = uri

        medias = await self.media_repository.add(medias)
        return [vars(media) for media in medias]

    async def delete(self, deletion_records: RecordList) -> None:
        records = validate({'*id': str}, deletion_records)
        medias = await self.media_repository.search([('id', 'in', [
            record['id'] for record in records])])

        for media in medias:
            await self.file_store_service.delete(media.uri)
        await self.media_repository.remove(medias)
