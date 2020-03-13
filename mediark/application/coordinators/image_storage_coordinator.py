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
        contents = self._extract_contents(image_records)
        images = await self.image_repository.add(
            [Image(**image_dict) for image_dict in image_records])

        contexts = [{'content': content, 'type': 'images', **vars(image)}
                    for image, content in zip(images, contents)]
        
        

        uris = await self.file_store_service.store(contexts)
        for image, uri in zip(images, uris):
            image.uri = uri

        await self.image_repository.add(images)

    def _extract_contents(self, image_records: RecordList) -> List[bytes]:
        contents: List[bytes] = []
        for image_dict in image_records:
            content = image_dict.pop('data', None)
            if not content:
                raise ValueError("All the images must have content.")
            contents.append(b64decode(content))
        return contents
