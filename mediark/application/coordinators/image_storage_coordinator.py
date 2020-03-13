from ..models import Image
from typing import List, Tuple, Dict, Any
from base64 import b64decode
from ..repositories import ImageRepository
from ..services import IdService, FileStoreService
from ..utilities import EntityNotFoundError
from .types import RecordList


class ImageStorageCoordinator:
    def __init__(self,
                 image_repository: ImageRepository,
                 id_service: IdService,
                 file_store_service: FileStoreService) -> None:
        self.image_repository = image_repository
        self.id_service = id_service
        self.file_store_service = file_store_service

    async def store(self, image_records: RecordList) -> None:
        contexts, image_records = self._build_contexts(image_records)
        images = await self.image_repository.add(
            [Image(**image_dict) for image_dict in image_records])

        uris = await self.file_store_service.store(contexts)
        for image, uri in zip(images, uris):
            image.uri = uri

        await self.image_repository.add(images)

    def _build_contexts(self, image_records: RecordList
                        ) -> Tuple[List[Dict[str, Any]], RecordList]:
        contexts: List[Dict[str, Any]] = []
        for image_dict in image_records:
            content = image_dict.pop('data', None)
            if not content:
                raise ValueError("All the images must have content.")
            image_dict.setdefault('id', self.id_service.generate_id())
            contexts.append({'content': b64decode(content), **image_dict})
        return contexts, image_records
