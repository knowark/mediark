from ..models import Image
from typing import List, Optional
from ..repositories import ImageRepository
from ..services import IdService, FileStoreService
from .types import ImageDict


class ImageStorageCoordinator:
    def __init__(self, image_repository: ImageRepository,
                 id_service: IdService,
                 file_store_service: FileStoreService) -> None:
        self.image_repository = image_repository
        self.id_service = id_service
        self.file_store_service = file_store_service

    async def store(self, image_dict: ImageDict) -> Optional[List[Image]]:
        if 'data' not in image_dict:
            return None

        if 'id' not in image_dict:
            image_dict['id'] = self.id_service.generate_id()

        file_id = str(image_dict.get('id'))
        content = image_dict.pop('data')
        extension = image_dict.get('extension')

        uri = self.file_store_service.store(file_id, content, extension)
        image_dict['uri'] = uri
        image = Image(**image_dict)
        return await self.image_repository.add(image)
